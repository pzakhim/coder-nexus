"""Unit tests for Clean Architecture validation engine and rule catalog."""

import pytest
from coder_nexus.architecture import (
    ArchitectureValidator,
    RULE_CATALOG,
    architecture_validator,
    strip_comments_and_strings,
)


def test_rule_sources_are_traceable_to_a_file_and_revision():
    for rule in RULE_CATALOG.values():
        assert any(prefix in rule.source_reference for prefix in ("docs/", ".agents/", "plugins/"))
        assert "@" in rule.source_reference


def test_strip_comments_and_strings_preserves_line_count():
    code = (
        "import 'package:flutter/material.dart';\n"
        "// this is a single line comment\n"
        "/*\n"
        " * multiline comment\n"
        " * with throw new Exception()\n"
        " */\n"
        "final str = 'throw inside string';\n"
        "final valid = 123;\n"
    )
    stripped = strip_comments_and_strings(code)

    assert code.count("\n") == stripped.count("\n")
    assert "this is a single line comment" not in stripped
    assert "multiline comment" not in stripped
    assert "throw inside string" not in stripped
    assert "final valid = 123;" in stripped


def test_validator_fails_fast_on_empty_code():
    res = architecture_validator.validate("", "domain")
    assert res["status"] == "error"
    assert "cannot be empty" in res["error"]

    res_ws = architecture_validator.validate("   \n\t ", "domain")
    assert res_ws["status"] == "error"
    assert "cannot be empty" in res_ws["error"]


def test_validator_fails_fast_on_invalid_layer():
    res = architecture_validator.validate("final x = 1;", "infrastructure")
    assert res["status"] == "error"
    assert "Invalid layer 'infrastructure'" in res["error"]
    assert "domain" in res["error"]


def test_validator_rejects_unbalanced_dart_and_never_claims_syntax_pass():
    malformed = architecture_validator.validate("class Broken {", "domain")
    assert malformed["status"] == "error"
    assert malformed["syntax_status"] == "INVALID"
    assert "Unbalanced" in malformed["error"]

    valid_shape = architecture_validator.validate("class Value {}", "domain")
    assert valid_shape["status"] == "success"
    assert valid_shape["syntax_status"] == "NOT_CHECKED"
    assert valid_shape["gate_status"] == "UNVERIFIED"
    assert any("Client analyzer" in item for item in valid_shape["unsupported_checks"])


def test_domain_rules_violations():
    # DOM-001: Flutter import
    # DOM-002: Data layer import
    # DOM-003: Mutable var field in Entity
    bad_domain_code = (
        "import 'package:flutter/material.dart';\n"
        "import '../data/models/user_model.dart';\n"
        "\n"
        "class UserEntity {\n"
        "  var name;\n"
        "  final String id;\n"
        "}\n"
    )
    res = architecture_validator.validate(bad_domain_code, "domain")
    assert res["status"] == "success"
    assert res["valid"] is False
    assert res["errors_count"] >= 2

    rule_ids = [v["rule_id"] for v in res["violations"]]
    assert "DOM-001" in rule_ids
    assert "DOM-002" in rule_ids
    assert "DOM-003" in rule_ids

    # Line numbers check
    dom_001_violation = next(v for v in res["violations"] if v["rule_id"] == "DOM-001")
    assert dom_001_violation["line_number"] == 1
    assert dom_001_violation["severity"] == "ERROR"
    assert "clean_architecture_rules.md" in dom_001_violation["source_reference"]

    dom_002_violation = next(v for v in res["violations"] if v["rule_id"] == "DOM-002")
    assert dom_002_violation["line_number"] == 2
    assert dom_002_violation["severity"] == "ERROR"


def test_domain_valid_code_passes():
    valid_domain_code = (
        "import 'package:equatable/equatable.dart';\n"
        "\n"
        "class UserEntity extends Equatable {\n"
        "  final String id;\n"
        "  final String name;\n"
        "\n"
        "  const UserEntity({required this.id, required this.name});\n"
        "\n"
        "  @override\n"
        "  List<Object?> get props => [id, name];\n"
        "}\n"
    )
    res = architecture_validator.validate(valid_domain_code, "domain")
    assert res["status"] == "success"
    assert res["valid"] is True
    assert res["errors_count"] == 0
    assert len(res["violations"]) == 0
    assert "DOM-001" in res["checked_rules"]


def test_data_rules_violations():
    # DAT-001: DataSource not extending BaseDataSource
    # DAT-002: RepoImpl not wrapping tryCatch or returning DataState
    # DAT-003: Model unsafe cast
    bad_data_code = (
        "class UserRemoteDataSource {\n"
        "  Future<void> fetch() async {}\n"
        "}\n"
        "\n"
        "class UserRepoImpl implements UserRepo {\n"
        "  Future<User> getUser() async {\n"
        "    return User();\n"
        "  }\n"
        "}\n"
        "\n"
        "class UserModel {\n"
        "  factory UserModel.fromJson(Map<String, dynamic> json) {\n"
        "    return UserModel(name: json['name'] as String);\n"
        "  }\n"
        "}\n"
    )
    res = architecture_validator.validate(bad_data_code, "data")
    assert res["status"] == "success"
    assert res["valid"] is False
    assert res["errors_count"] >= 2

    rule_ids = [v["rule_id"] for v in res["violations"]]
    assert "DAT-001" in rule_ids
    assert "DAT-002" in rule_ids
    assert "DAT-003" in rule_ids


def test_data_valid_code_passes():
    valid_data_code = (
        "import 'package:app_core/app_core.dart';\n"
        "\n"
        "class UserRemoteDataSource extends BaseDataSource {\n"
        "  UserRemoteDataSource(super.apiClient);\n"
        "}\n"
        "\n"
        "class UserRepoImpl implements UserRepo {\n"
        "  final UserRemoteDataSource dataSource;\n"
        "  UserRepoImpl(this.dataSource);\n"
        "\n"
        "  @override\n"
        "  Future<DataState<UserEntity>> getUser() async {\n"
        "    return await tryCatchAsync<UserEntity>(() async {\n"
        "      final res = await dataSource.fetch();\n"
        "      return DataSuccess(res.toEntity());\n"
        "    });\n"
        "  }\n"
        "}\n"
    )
    res = architecture_validator.validate(valid_data_code, "data")
    assert res["status"] == "success"
    assert res["valid"] is True
    assert res["errors_count"] == 0


def test_data_rules_do_not_borrow_evidence_from_other_classes():
    code = (
        "class Helper {\n"
        "  Future<DataState<User>> load() => source.get().tryCatch((r) => DataSuccess(r));\n"
        "}\n"
        "class UserRepoImpl {\n"
        "  Future<User> getUser() async => User();\n"
        "}\n"
    )
    res = architecture_validator.validate(code, "data")
    assert "DAT-002" in [v["rule_id"] for v in res["violations"]]


def test_indirect_data_source_inheritance_is_unverified_not_error():
    code = (
        "abstract class UserDataSource extends BaseDataSource {}\n"
        "class UserDataSourceImpl extends UserDataSource {}\n"
    )
    res = architecture_validator.validate(code, "data")
    dat_001 = [v for v in res["violations"] if v["rule_id"] == "DAT-001"]
    assert len(dat_001) == 1
    assert dat_001[0]["severity"] == "WARNING"
    assert res["valid"] is True
    assert res["gate_status"] == "UNVERIFIED"


def test_presentation_rules_violations():
    # PRE-001: Throw in presentation
    # PRE-002: State not extending BaseBlocState
    # PRE-003: Controller created without dispose()
    # PRE-004: Raw primitive widget (ElevatedButton)
    # RTE-001: Missing @RoutePage
    bad_pres_code = (
        "import 'package:auto_route/auto_route.dart';\n"
        "class LoginState {\n"
        "  final bool isLoading;\n"
        "  LoginState(this.isLoading);\n"
        "}\n"
        "\n"
        "class _LoginScreenState extends State<LoginScreen> {\n"
        "  final controller = TextEditingController();\n"
        "  void submit() {\n"
        "    throw Exception('UI crash');\n"
        "  }\n"
        "  @override\n"
        "  Widget build(BuildContext context) {\n"
        "    return ElevatedButton(onPressed: submit, child: Text('Go'));\n"
        "  }\n"
        "}\n"
        "\n"
        "class LoginScreen extends StatefulWidget {}\n"
    )
    res = architecture_validator.validate(bad_pres_code, "presentation")
    assert res["status"] == "success"
    assert res["valid"] is False

    rule_ids = [v["rule_id"] for v in res["violations"]]
    assert "PRE-001" in rule_ids
    assert "PRE-002" in rule_ids
    assert "PRE-003" in rule_ids
    assert "PRE-004" in rule_ids
    assert "RTE-001" in rule_ids

    pre_001 = next(v for v in res["violations"] if v["rule_id"] == "PRE-001")
    assert pre_001["severity"] == "ERROR"


def test_pattern_a_concrete_states_are_not_warned():
    code = (
        "sealed class AuthState extends BaseBlocState {}\n"
        "final class LoginAuthSuccessState extends AuthState {}\n"
    )
    res = architecture_validator.validate(code, "presentation")
    assert "PRE-002" not in [v["rule_id"] for v in res["violations"]]


def test_each_stateful_widget_must_dispose_its_own_resources():
    code = (
        "class _FirstState extends State<First> {\n"
        "  final first = TextEditingController();\n"
        "  void dispose() { first.dispose(); super.dispose(); }\n"
        "}\n"
        "class _SecondState extends State<Second> {\n"
        "  final second = TextEditingController();\n"
        "}\n"
    )
    res = architecture_validator.validate(code, "presentation")
    findings = [v for v in res["violations"] if v["rule_id"] == "PRE-003"]
    assert len(findings) == 1
    assert findings[0]["line_number"] == 5


def test_dispose_method_must_release_each_owned_resource():
    code = (
        "class _FormState extends State<Form> {\n"
        "  late final TextEditingController controller;\n"
        "  void initState() { controller = TextEditingController(); }\n"
        "  void dispose() { super.dispose(); }\n"
        "}\n"
    )
    res = architecture_validator.validate(code, "presentation")
    findings = [v for v in res["violations"] if v["rule_id"] == "PRE-003"]
    assert len(findings) == 1
    assert "controller" in findings[0]["message"]


def test_route_annotation_must_belong_to_the_screen_declaration():
    code = (
        "import 'package:auto_route/auto_route.dart';\n"
        "@RoutePage()\n"
        "class Helper {}\n"
        "class LoginScreen extends StatelessWidget {}\n"
    )
    res = architecture_validator.validate(code, "presentation")
    assert "RTE-001" in [v["rule_id"] for v in res["violations"]]


def test_screen_contract_accepts_base_and_exempts_dialog():
    code = (
        "class LoginScreen extends BaseScreen {\n"
        "  BaseScreenState<LoginScreen> createState() => _LoginScreenState();\n"
        "  ScreenModel getScreen() => AppScreen.login;\n"
        "}\n"
        "class _LoginScreenState extends BaseScreenState<LoginScreen> {\n"
        "  Widget buildMobilePortrait() => const Placeholder();\n"
        "}\n"
        "class ConfirmDialog extends StatefulWidget {}\n"
        "class _ConfirmDialogState extends State<ConfirmDialog> {}\n"
    )
    res = architecture_validator.validate(code, "presentation")
    assert not {"PRE-002", "PRE-005", "PRE-006", "RTE-001"} & {
        v["rule_id"] for v in res["violations"]
    }
    assert res["gate_status"] == "UNVERIFIED"


def test_base_screen_state_must_dispose_owned_controller():
    code = (
        "class LoginScreen extends BaseScreen {}\n"
        "class _LoginScreenState extends BaseScreenState<LoginScreen> {\n"
        "  final controller = TextEditingController();\n"
        "}\n"
    )
    res = architecture_validator.validate(code, "presentation")
    assert "PRE-003" in [v["rule_id"] for v in res["violations"]]
    assert "PRE-002" not in [v["rule_id"] for v in res["violations"]]


def test_go_router_screen_does_not_require_auto_route_annotation():
    code = (
        "import 'package:go_router/go_router.dart';\n"
        "class LoginScreen extends BaseScreen {}\n"
    )
    res = architecture_validator.validate(code, "presentation")
    assert "RTE-001" not in [v["rule_id"] for v in res["violations"]]


def test_page_screen_and_native_state_are_rejected():
    code = (
        "class LoginPage extends StatefulWidget {\n"
        "  State<LoginPage> createState() => _LoginPageState();\n"
        "}\n"
        "class _LoginPageState extends State<LoginPage> {}\n"
    )
    res = architecture_validator.validate(code, "presentation")
    ids = [v["rule_id"] for v in res["violations"]]
    assert "PRE-005" in ids
    assert ids.count("PRE-006") == 2
    assert res["gate_status"] == "FAILED"


def test_qualified_base_hooks_require_client_source():
    code = "class HomeScreen extends app.BaseScreen {}\n"
    res = architecture_validator.validate(code, "presentation")
    issues = [v for v in res["violations"] if v["rule_id"] == "PRE-006"]
    assert issues == []
    assert any("package resolution" in item for item in res["unsupported_checks"])


def test_indirect_screen_base_needs_client_resolution():
    code = "class DetailScreen extends TrackedScreen {}\n"
    res = architecture_validator.validate(code, "presentation")
    issues = [v for v in res["violations"] if v["rule_id"] == "PRE-006"]
    assert len(issues) == 1
    assert issues[0]["severity"] == "WARNING"
    assert res["gate_status"] == "UNVERIFIED"


def test_commented_base_is_not_recognized_as_a_live_declaration():
    code = "// class LoginScreen extends BaseScreen {}\nclass ConfirmDialog extends StatelessWidget {}\n"
    res = architecture_validator.validate(code, "presentation")
    assert "PRE-006" not in [v["rule_id"] for v in res["violations"]]


def test_screen_registry_without_widget_parent_is_not_a_screen():
    code = "class AppScreen extends Equatable {}\n"
    res = architecture_validator.validate(code, "presentation")
    assert not {"PRE-005", "PRE-006"} & {v["rule_id"] for v in res["violations"]}


def test_style_print_violation():
    code_with_print = (
        "class Helper {\n"
        "  void run() {\n"
        "    print('debug log');\n"
        "  }\n"
        "}\n"
    )
    res = architecture_validator.validate(code_with_print, "domain")
    assert res["status"] == "success"
    rule_ids = [v["rule_id"] for v in res["violations"]]
    assert "STY-001" in rule_ids
    assert res["violations"][0]["line_number"] == 3


def test_di_singleton_cubit_lifetime_is_unverified():
    code_di = (
        "void diUserModule(GetIt injector) {\n"
        "  injector.registerLazySingleton(() => UserCubit(injector()));\n"
        "}\n"
    )
    res = architecture_validator.validate(code_di, "module")
    assert res["status"] == "success"
    rule_ids = [v["rule_id"] for v in res["violations"]]
    assert "DIR-001" not in rule_ids
    assert any("UserCubit" in item and "lifetime" in item for item in res["unsupported_checks"])


def test_domain_export_and_typed_mutable_field_are_detected():
    code = (
        "export 'package:flutter/widgets.dart';\n"
        "class UserEntity {\n"
        "  String name;\n"
        "  UserEntity(this.name);\n"
        "}\n"
    )
    res = architecture_validator.validate(code, "domain")
    rule_ids = [v["rule_id"] for v in res["violations"]]
    assert "DOM-001" in rule_ids
    assert "DOM-003" in rule_ids


def test_false_positive_resistance():
    # Comments and strings should not trigger violations even if they contain forbidden tokens
    tricky_code = (
        "// import 'package:flutter/material.dart';\n"
        "/*\n"
        " * print('hello');\n"
        " * throw Exception('never');\n"
        " */\n"
        "class SafeEntity extends Equatable {\n"
        "  final String debugMsg = \"print('hi') and throw Exception()\";\n"
        "  final String flutterRef = \"package:flutter/material.dart\";\n"
        "  const SafeEntity();\n"
        "  @override\n"
        "  List<Object?> get props => [debugMsg, flutterRef];\n"
        "}\n"
    )
    res = architecture_validator.validate(tricky_code, "domain")
    assert res["status"] == "success"
    assert res["valid"] is True
    assert len(res["violations"]) == 0
