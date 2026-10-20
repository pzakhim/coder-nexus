"""Profile routing must preserve common checks without imposing company foundations."""

import pytest

from coder_nexus.architecture.module_validator import module_architecture_validator
from coder_nexus.architecture.validator import architecture_validator
from coder_nexus.server import app


SCREEN = """class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});
  @override
  Widget build(BuildContext context) => TextField();
}
"""


@pytest.mark.parametrize("profile", ["imespro", "external-structured", "external-standard"])
def test_standard_screen_respects_selected_profile(profile):
    result = architecture_validator.validate(SCREEN, "presentation", profile)
    assert result["architecture_profile"] == profile
    rules = {v["rule_id"] for v in result["violations"]}
    if profile == "imespro":
        assert result["gate_status"] == "FAILED"
        assert {"PRE-006", "PRE-004"} <= rules
    else:
        assert result["valid"]
        assert result["gate_status"] == "UNVERIFIED"
        assert not {"PRE-006", "PRE-004", "PRE-005"} & set(result["checked_rules"])


@pytest.mark.parametrize("profile", ["external-structured", "external-standard"])
def test_external_foundations_do_not_require_company_result_state_or_logger(profile):
    data = architecture_validator.validate(
        "class OrdersDataSource {}\nclass OrdersRepoImpl { Future<int> count() async => 1; }", "data", profile,
    )
    assert data["valid"]
    assert not {"DAT-001", "DAT-002"} & set(data["checked_rules"])
    ui = architecture_validator.validate("class OrdersState {}\nvoid trace() { print(1); }", "presentation", profile)
    assert not {"PRE-002", "STY-001"} & set(ui["checked_rules"])


@pytest.mark.parametrize("profile", ["imespro", "external-structured", "external-standard"])
def test_common_domain_and_lifecycle_checks_survive_profile_routing(profile):
    domain = architecture_validator.validate(
        "import 'package:flutter/material.dart';\nimport '../data/order.dart';\nclass OrderEntity {}", "domain", profile,
    )
    assert {"DOM-001", "DOM-002"} <= {v["rule_id"] for v in domain["violations"]}
    ui = architecture_validator.validate(
        "class _HomeState extends State<HomeScreen> { final controller = TextEditingController(); }", "presentation", profile,
    )
    assert "PRE-003" in {v["rule_id"] for v in ui["violations"]}


@pytest.mark.parametrize("profile", ["external-structured", "external-standard"])
def test_external_module_allows_client_layout_but_keeps_domain_boundaries(profile):
    files = {"views/home_page.dart": SCREEN, "domain/order.dart": "class Order {}"}
    result = module_architecture_validator.validate_module(
        file_paths=list(files), files_content=files, architecture_profile=profile,
    )
    assert result["valid"]
    assert result["gate_status"] == "UNVERIFIED"
    assert not {"MOD-001", "MOD-002", "MOD-004", "PRE-006"} & set(result["checked_rules"])
    files["domain/order.dart"] = "import '../data/order.dart';\nclass Order {}"
    result = module_architecture_validator.validate_module(
        file_paths=list(files), files_content=files, architecture_profile=profile,
    )
    assert result["gate_status"] == "FAILED"
    assert any(v["rule_id"] == "DOM-002" for v in result["violations"])


def test_omitted_profile_retains_legacy_checks_and_unknown_profile_fails():
    assert architecture_validator.validate(SCREEN, "presentation")["gate_status"] == "FAILED"
    assert architecture_validator.validate(SCREEN, "presentation", "external-typo")["status"] == "error"
    assert module_architecture_validator.validate_module(architecture_profile="external-typo")["status"] == "error"


@pytest.mark.anyio
async def test_profile_is_exposed_and_forwarded_by_both_mcp_tools(tmp_path):
    tools = {t.name: t for t in await app.list_tools()}
    for name in ("validate_architecture_code", "validate_module_architecture"):
        assert tools[name].input_schema["properties"]["architecture_profile"]["default"] == "imespro"
    result = await app.call_tool("validate_architecture_code", {
        "dart_code": SCREEN, "layer": "presentation", "architecture_profile": "external-standard",
    })
    assert not result.is_error
    assert '"valid": true' in result.content[0].text
    (tmp_path / "home.dart").write_text(SCREEN)
    result = await app.call_tool("validate_module_architecture", {
        "module_path": str(tmp_path), "architecture_profile": "external-structured",
    })
    assert not result.is_error
    assert '"gate_status": "UNVERIFIED"' in result.content[0].text
    assert '"valid": true' in result.content[0].text
