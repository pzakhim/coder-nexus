"""Tests for ModuleArchitectureValidator (Whole-module Clean Architecture inspection)."""

import pytest
from coder_nexus.architecture.module_validator import module_architecture_validator


VALID_MODULE_FILES = [
    "di.dart",
    "domain/entities/auth_session_entity.dart",
    "domain/repo/auth_repository.dart",
    "domain/usecases/login_usecase.dart",
    "data/data_sources/auth_remote_data_source.dart",
    "data/models/auth_session_model.dart",
    "data/mappers/auth_mapper.dart",
    "data/repo_impl/auth_repo_impl.dart",
    "presentation/bloc/login_cubit.dart",
    "presentation/bloc/login_state.dart",
    "presentation/screens/login_screen.dart",
    "presentation/widgets/auth_header_widget.dart",
]

VALID_DI_CONTENT = """import 'package:get_it/get_it.dart';
import 'data/mappers/auth_mapper.dart';
import 'data/data_sources/auth_remote_data_source.dart';
import 'domain/repo/auth_repository.dart';
import 'data/repo_impl/auth_repo_impl.dart';
import 'domain/usecases/login_usecase.dart';
import 'presentation/bloc/login_cubit.dart';

void diAuthModule(GetIt injector) {
  // 1. Mapper
  injector.registerLazySingleton(() => AuthMapper());

  // 2. DataSource
  injector.registerLazySingleton(() => AuthRemoteDataSource(injector()));

  // 3. Repository
  injector.registerLazySingleton<AuthRepository>(() => AuthRepoImpl(injector(), injector()));

  // 4. UseCases
  injector.registerLazySingleton(() => LoginUseCase(injector()));

  // 5. Cubits
  injector.registerFactory(() => LoginCubit(injector()));
}
"""


def test_validate_module_with_incomplete_source_is_unverified():
    """A file inventory cannot prove checks for source it does not contain."""
    contents = {
        "di.dart": VALID_DI_CONTENT,
        "domain/entities/auth_session_entity.dart": "class AuthSessionEntity {}",
    }
    res = module_architecture_validator.validate_module(
        feature_name="auth",
        file_paths=VALID_MODULE_FILES,
        files_content=contents,
    )
    assert res["status"] == "success"
    assert res["valid"] is True
    assert res["gate_status"] == "UNVERIFIED"
    assert res["errors_count"] == 0
    assert any(v["rule_id"] == "MOD-005-MISSING-SOURCE" for v in res["violations"])


def test_validate_module_missing_domain_layer():
    """Verify that a module missing domain layer fails with MOD-001."""
    files = [f for f in VALID_MODULE_FILES if not f.startswith("domain/")]
    res = module_architecture_validator.validate_module(
        feature_name="auth",
        file_paths=files,
        files_content={"di.dart": VALID_DI_CONTENT},
    )
    assert res["valid"] is False
    assert any("MOD-001-MISSING-DOMAIN" in v["rule_id"] for v in res["violations"])


def test_validate_module_forbidden_views_dir():
    """Verify that placing views/ directly under module root is rejected."""
    files = VALID_MODULE_FILES + ["views/login_screen.dart", "views/forgot_screen.dart"]
    res = module_architecture_validator.validate_module(
        feature_name="auth",
        file_paths=files,
        files_content={"di.dart": VALID_DI_CONTENT},
    )
    assert res["valid"] is False
    assert any("MOD-002-FORBIDDEN-VIEWS-DIR" in v["rule_id"] for v in res["violations"])


def test_validate_module_domain_flutter_import():
    """Verify that domain files importing package:flutter/ are rejected."""
    contents = {
        "di.dart": VALID_DI_CONTENT,
        "domain/entities/auth_session_entity.dart": "import 'package:flutter/material.dart';\nclass AuthSessionEntity {}",
    }
    res = module_architecture_validator.validate_module(
        feature_name="auth",
        file_paths=VALID_MODULE_FILES,
        files_content=contents,
    )
    assert res["valid"] is False
    assert any("MOD-003-DOMAIN-FLUTTER-IMPORT" in v["rule_id"] for v in res["violations"])


def test_validate_module_incomplete_di_registration():
    """Verify that di.dart missing registration steps is flagged."""
    incomplete_di = """void diAuthModule(GetIt injector) {
  injector.registerFactory(() => LoginCubit(injector()));
}"""
    contents = {
        "di.dart": incomplete_di,
        "domain/entities/auth_session_entity.dart": "class AuthSessionEntity {}",
    }
    res = module_architecture_validator.validate_module(
        feature_name="auth",
        file_paths=VALID_MODULE_FILES,
        files_content=contents,
    )
    assert any("MOD-004-INCOMPLETE-DI-REGISTRATION" in v["rule_id"] for v in res["violations"])
    assert res["gate_status"] == "UNVERIFIED"


def test_module_rejects_page_directory_and_native_screen():
    files = [p for p in VALID_MODULE_FILES if not p.startswith("presentation/screens/")]
    files.append("presentation/pages/login_page.dart")
    res = module_architecture_validator.validate_module(
        feature_name="auth", file_paths=files,
        files_content={
            "di.dart": VALID_DI_CONTENT,
            "presentation/pages/login_page.dart": "class LoginPage extends StatefulWidget {}",
        },
    )
    ids = {v["rule_id"] for v in res["violations"]}
    assert {"MOD-006-LEGACY-PAGE", "PRE-005", "PRE-006"} <= ids
    assert res["gate_status"] == "UNVERIFIED"


def test_module_screen_declaration_does_not_prove_runtime_tracking():
    screen = (
        "class LoginScreen extends BaseScreen {\n"
        "  BaseScreenState<LoginScreen> createState() => _LoginScreenState();\n"
        "  ScreenModel getScreen() => AppScreen.login;\n"
        "}\n"
        "class _LoginScreenState extends BaseScreenState<LoginScreen> {}\n"
    )
    contents = {path: "class Placeholder {}" for path in VALID_MODULE_FILES}
    contents["di.dart"] = VALID_DI_CONTENT
    contents["presentation/screens/login_screen.dart"] = screen
    res = module_architecture_validator.validate_module(
        feature_name="auth", file_paths=VALID_MODULE_FILES, files_content=contents,
    )
    assert res["valid"] is True
    assert res["gate_status"] == "UNVERIFIED"
    assert not [v for v in res["violations"] if v["rule_id"] in {"PRE-005", "PRE-006"}]
    assert any("tracking" in item for item in res["unsupported_checks"])


@pytest.mark.parametrize(
    "path,code,expected",
    [
        ("presentation/widgets/login_screen.dart", "class LoginScreen extends StatefulWidget {}", "MOD-006-SCREEN-PATH"),
        ("presentation/login_screen.dart", "class LoginScreen extends BaseScreen {}", "MOD-006-SCREEN-PATH"),
        ("presentation/screens/login_screen.dart", "class LoginView extends StatefulWidget {}", "MOD-006-MISSING-SCREEN"),
    ],
)
def test_screen_path_and_declaration_cannot_evade_contract(path, code, expected):
    files = [p for p in VALID_MODULE_FILES if p != "presentation/screens/login_screen.dart"] + [path]
    res = module_architecture_validator.validate_module(
        feature_name="auth", file_paths=files,
        files_content={"di.dart": VALID_DI_CONTENT, path: code},
    )
    assert expected in {v["rule_id"] for v in res["violations"]}
    assert res["gate_status"] == "FAILED"


def test_framework_route_page_is_not_a_screen():
    path = "presentation/routes/fade_page.dart"
    res = module_architecture_validator.validate_module(
        feature_name="auth", file_paths=VALID_MODULE_FILES + [path],
        files_content={"di.dart": VALID_DI_CONTENT, path: "class FadePage extends Page<void> {}"},
    )
    assert not [v for v in res["violations"] if v["file_path"] == path]


def test_screen_registry_is_not_a_destination():
    path = "presentation/registry/app_screen.dart"
    res = module_architecture_validator.validate_module(
        feature_name="auth", file_paths=VALID_MODULE_FILES + [path],
        files_content={"di.dart": VALID_DI_CONTENT, path: "class AppScreen extends Equatable {}"},
    )
    assert not [v for v in res["violations"] if v["file_path"] == path]


def test_local_base_stub_does_not_count_as_a_screen():
    path = "presentation/screens/login_screen.dart"
    res = module_architecture_validator.validate_module(
        feature_name="auth", file_paths=VALID_MODULE_FILES,
        files_content={"di.dart": VALID_DI_CONTENT, path: "class BaseScreen extends StatefulWidget {}"},
    )
    assert "MOD-006-MISSING-SCREEN" in {v["rule_id"] for v in res["violations"]}
