"""Project structure and Clean Architecture blueprint generator.

Strictly READ-ONLY: Never writes or scaffolds files directly into the Flutter workspace.
Generates architectural blueprints and guidelines with traceable sources.
"""

import re
from typing import Any

FEATURE_NAME_REGEX = re.compile(r"^[a-z][a-z0-9_]*$")


def get_project_structure_data(scope: str, feature_name: str = "") -> dict[str, Any]:
    """Generate architecture blueprint for root project or a specific feature module.

    Args:
        scope: Either 'root' (top-level layout & boot sequence) or 'module' (feature module).
        feature_name: Name of the feature module in lower_snake_case (required if scope='module').

    Returns:
        Dictionary containing status, blueprint layout, and rules.
    """
    clean_scope = (scope or "").strip().lower()
    clean_feature_name = (feature_name or "").strip()

    if clean_scope == "root":
        if clean_feature_name:
            return {
                "status": "error",
                "error": "feature_name should not be provided when scope is 'root'.",
            }
        return _build_root_blueprint()

    if clean_scope == "module":
        if not clean_feature_name:
            return {
                "status": "error",
                "error": "feature_name is required when scope is 'module'.",
            }

        # Guard against path traversal and separators
        if ".." in clean_feature_name or "/" in clean_feature_name or "\\" in clean_feature_name:
            return {
                "status": "error",
                "error": (
                    f"Invalid feature_name '{clean_feature_name}': path traversal and "
                    "directory separators are strictly forbidden."
                ),
            }

        # Guard naming convention: lower_snake_case
        if not FEATURE_NAME_REGEX.match(clean_feature_name):
            return {
                "status": "error",
                "error": (
                    f"Invalid feature_name '{clean_feature_name}': must be valid lower_snake_case "
                    "matching '^[a-z][a-z0-9_]*$'."
                ),
            }

        return _build_module_blueprint(clean_feature_name)

    return {
        "status": "error",
        "error": f"Unsupported scope '{clean_scope}'. Supported scopes are 'root' and 'module'.",
    }


def _build_root_blueprint() -> dict[str, Any]:
    return {
        "status": "success",
        "scope": "root",
        "description": "Enterprise Flutter Clean Architecture Root & Subsystem Blueprint",
        "blueprint_tree": {
            "lib/": {
                "main_dev.dart": "Entry point for flavor dev (API dev, banner ON)",
                "main_stage.dart": "Entry point for flavor stage (API stage, banner ON)",
                "main_prod.dart": "Entry point for flavor prod (API prod, banner OFF)",
                "main.dart": "Bootstrap logic calling runZonedGuarded and initializing services",
                "app.dart": "Root MaterialApp & Router configuration with routeObserver",
                "core/": {
                    "config/": "App-level configuration and flavor settings (FlavorConfig, ApiConfig)",
                    "routes/": "Application router registry, route guards, and path constants",
                    "di/": "Service locator root setup and core DI registration",
                    "constants/": "Project-specific global constants, storage keys, and error codes",
                    "shared/": "Project-specific shared widgets or helpers used by >= 2 modules (Core gaps)",
                },
                "modules/": {
                    "modules_di.dart": "Composition root registering all module DI functions",
                    "<feature>/": "Feature modules following 3-layer Clean Architecture (domain, data, presentation)",
                },
            }
        },
        "external_core_libraries": {
            "app_core": "BaseScreen, UseCasePower, ListViewPaging, BaseRemoteDataSource, DataMapper",
            "app_util": "DataState, ApiService, tryCatch, LocalStorageService, DeviceHelper, parse_util",
            "app_ui_kit": "Design-system components (buttons, form fields, dialogs, empty/loading states, colors)",
        },
        "boot_sequence": [
            "1. Host setup: Firebase.initializeApp(), MatomoTracker.instance.initialize(...) (app_core GUIDE §3)",
            "2. Core services DI: DeviceHelper (awaited), LocalStorageService, FlavorConfig/ApiConfig, ApiService (app_util GUIDE §3)",
            "3. Feature Modules DI: lib/modules/modules_di.dart",
            "4. Root App: MaterialApp with routeObserver and AppLocalization inside EasyLocalization",
        ],
        "sources": [
            "plugins/packs/flutter/rules/clean_architecture_rules.md",
            "plugins/packs/flutter/skills/core-usage/SKILL.md",
            "../app-core/guidance/GUIDE.md",
            "../app-util/guidance/GUIDE.md",
            "../app-ui-kit/guidance/GUIDE.md",
        ],
    }


def _build_module_blueprint(feature: str) -> dict[str, Any]:
    pascal_feature = "".join(part.capitalize() for part in feature.split("_"))
    return {
        "status": "success",
        "scope": "module",
        "feature_name": feature,
        "pascal_case_name": pascal_feature,
        "description": f"Clean Architecture 3-Layer Blueprint for module '{feature}'",
        "blueprint_tree": {
            f"lib/modules/{feature}/": {
                "di.dart": f"di{pascal_feature}Module(GetIt injector) registration",
                "domain/": {
                    "entities/": f"{feature}_entity.dart (Pure Dart, immutable, Equatable)",
                    "repo/": f"{feature}_repository.dart (Abstract contract returning DataState<T>)",
                    "usecases/": f"get_{feature}_usecase.dart (Callable business actions via UseCasePower)",
                },
                "data/": {
                    "data_sources/": f"{feature}_data_source.dart (Extends BaseRemoteDataSource, calls ApiService)",
                    "models/": f"{feature}_model.dart (DTO parsed with parse_util, implements DataMapper)",
                    "mappers/": f"{feature}_mapper.dart (Model -> Entity mapping)",
                    "repo_impl/": f"{feature}_repo_impl.dart (Implements repo, wraps .tryCatch)",
                },
                "presentation/": {
                    "bloc/": [
                        f"{feature}_cubit.dart (Injects UseCase, manages state)",
                        f"{feature}_state.dart (Cubit state following Client convention: sealed classes or Equatable)",
                    ],
                    "screens/": (
                        f"{feature}_screen.dart ({pascal_feature}Screen extends BaseScreen / BaseScreenState, "
                        "screen metadata getScreen() and buildMobilePortrait(); never overrides build())"
                    ),
                    "widgets/": "Feature-specific widgets",
                },
            }
        },
        "di_registration_order": [
            f"1. Mapper: injector.registerLazySingleton(() => {pascal_feature}Mapper())",
            f"2. DataSource: injector.registerLazySingleton(() => {pascal_feature}DataSource(...))",
            f"3. Repository: injector.registerLazySingleton<{pascal_feature}Repository>(() => {pascal_feature}RepoImpl(...))",
            f"4. UseCases: injector.registerLazySingleton(() => Get{pascal_feature}UseCase(...))",
            f"5. Cubits: injector.registerFactory(() => {pascal_feature}Cubit(...))",
        ],
        "composition_root": "Must be registered in lib/modules/modules_di.dart",
        "sources": [
            "plugins/packs/flutter/rules/clean_architecture_rules.md",
            "plugins/packs/flutter/skills/core-usage/SKILL.md",
            "../app-core/guidance/GUIDE.md",
            "../app-util/guidance/GUIDE.md",
            "../app-ui-kit/guidance/GUIDE.md",
        ],
    }
