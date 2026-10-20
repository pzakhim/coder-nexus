"""Unit tests for Clean Architecture project structure generator."""

import pytest
from coder_nexus.architecture.structure import get_project_structure_data


def test_get_project_structure_root_success():
    """Verify scope='root' returns top-level layout, boot sequence, and sources."""
    res = get_project_structure_data(scope="root")
    assert res["status"] == "success"
    assert res["scope"] == "root"
    assert "blueprint_tree" in res
    assert "lib/" in res["blueprint_tree"]
    assert len(res["boot_sequence"]) == 4
    assert len(res["sources"]) > 0
    assert "pages/" not in res["blueprint_tree"]["lib/"]


def test_get_project_structure_root_rejects_feature_name():
    """Verify scope='root' fails if feature_name is provided."""
    res = get_project_structure_data(scope="root", feature_name="auth")
    assert res["status"] == "error"
    assert "feature_name should not be provided" in res["error"]


def test_get_project_structure_module_success():
    """Verify scope='module' with valid lower_snake_case feature_name returns 3-layer blueprint."""
    res = get_project_structure_data(scope="module", feature_name="order_history")
    assert res["status"] == "success"
    assert res["scope"] == "module"
    assert res["feature_name"] == "order_history"
    assert res["pascal_case_name"] == "OrderHistory"
    assert "lib/modules/order_history/" in res["blueprint_tree"]
    assert len(res["di_registration_order"]) == 5
    assert len(res["sources"]) > 0
    screen = res["blueprint_tree"]["lib/modules/order_history/"]["presentation/"]["screens/"]
    assert "OrderHistoryScreen" in screen
    assert "BaseScreenState" in screen


def test_get_project_structure_module_missing_name():
    """Verify scope='module' requires feature_name."""
    res = get_project_structure_data(scope="module", feature_name="")
    assert res["status"] == "error"
    assert "feature_name is required" in res["error"]


@pytest.mark.parametrize(
    "invalid_name",
    [
        "OrderHistory",      # PascalCase
        "order-history",     # kebab-case
        "123orders",         # starts with digit
        "order history",     # contains space
        "order@feature",     # invalid character
    ],
)
def test_get_project_structure_module_invalid_naming(invalid_name):
    """Verify non-snake_case names are rejected."""
    res = get_project_structure_data(scope="module", feature_name=invalid_name)
    assert res["status"] == "error"
    assert "must be valid lower_snake_case" in res["error"]


@pytest.mark.parametrize(
    "traversal_name",
    [
        "../escape",
        "nested/submodule",
        r"nested\submodule",
        "..",
    ],
)
def test_get_project_structure_module_path_traversal(traversal_name):
    """Verify path traversal attacks and slashes are strictly blocked."""
    res = get_project_structure_data(scope="module", feature_name=traversal_name)
    assert res["status"] == "error"
    assert "forbidden" in res["error"] or "must be valid lower_snake_case" in res["error"]


def test_get_project_structure_unsupported_scope():
    """Verify unrecognized scope returns a clear error."""
    res = get_project_structure_data(scope="invalid_scope")
    assert res["status"] == "error"
    assert "Unsupported scope" in res["error"]
