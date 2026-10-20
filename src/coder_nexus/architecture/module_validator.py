"""Module architecture validator for Flutter Clean Architecture enforcement.

Inspects feature module directory structure, checks presence of 3 layers (Domain,
Data, Presentation), verifies di.dart registration order, ensures pure Dart in Domain,
and forbids non-standard horizontal 'views/' directories.
"""

from dataclasses import dataclass
import os
from pathlib import Path
import re
from typing import Any, Optional

from .validator import (
    ARCHITECTURE_PROFILES,
    NON_WIDGET_SCREEN_SUPERCLASSES,
    _class_blocks,
    architecture_validator,
    strip_comments_and_strings,
)


@dataclass(frozen=True)
class ModuleViolation:
    rule_id: str
    severity: str  # "ERROR" | "WARNING"
    file_path: Optional[str]
    line_number: Optional[int]
    message: str
    suggestion: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "message": self.message,
            "suggestion": self.suggestion,
        }


class ModuleArchitectureValidator:
    """Validator engine verifying whole-module Clean Architecture compliance."""

    def validate_module(
        self,
        module_path: str = "",
        feature_name: str = "",
        file_paths: Optional[list[str]] = None,
        files_content: Optional[dict[str, str]] = None,
        architecture_profile: str = "imespro",
    ) -> dict[str, Any]:
        """Validate a Flutter feature module directory against Clean Architecture rules.

        Args:
            module_path: Path to `lib/modules/<feature>/`.
            feature_name: Optional feature name.
            file_paths: Optional list of relative file paths for in-memory/test validation.
            files_content: Optional mapping of relative path to content.
            architecture_profile: Approved foundation profile; defaults to legacy iMESPro checks.

        Returns:
            Dictionary with status, valid flag, violations count, and structured violations.
        """
        if architecture_profile not in ARCHITECTURE_PROFILES:
            return {"status": "error", "error": f"Unknown architecture_profile: {architecture_profile!r}."}
        violations: list[ModuleViolation] = []
        checked_rules: list[str] = []

        # Determine relative paths and contents
        resolved_files: set[str] = set()
        resolved_contents: dict[str, str] = dict(files_content or {})
        unreadable_files: list[str] = []

        p = Path(module_path) if module_path else None
        if p and p.exists() and p.is_dir():
            for root, _, files in os.walk(p):
                for f in files:
                    if f.endswith(".dart"):
                        full_f = Path(root) / f
                        rel_f = str(full_f.relative_to(p))
                        resolved_files.add(rel_f)
                        try:
                            resolved_contents[rel_f] = full_f.read_text(encoding="utf-8")
                        except (OSError, UnicodeError):
                            unreadable_files.append(rel_f)
            if not feature_name:
                feature_name = p.name
        elif file_paths:
            resolved_files = set(file_paths)

        if not resolved_files:
            return {
                "status": "error",
                "error": f"No Dart files found in module path '{module_path}' or file_paths is empty.",
            }

        if unreadable_files:
            return {
                "status": "error",
                "error": f"Unable to read Dart files: {', '.join(sorted(unreadable_files))}.",
            }

        missing_content = sorted(path for path in resolved_files if not resolved_contents.get(path, "").strip())
        if missing_content:
            violations.append(
                ModuleViolation(
                    rule_id="MOD-005-MISSING-SOURCE",
                    severity="WARNING",
                    file_path=None,
                    line_number=None,
                    message=f"Source content unavailable for {len(missing_content)} Dart files: {', '.join(missing_content)}.",
                    suggestion="Provide complete module source before approving architecture checks.",
                )
            )

        if not feature_name and module_path:
            feature_name = Path(module_path).name

        if architecture_profile == "imespro":
            checked_rules.extend(("MOD-001", "MOD-002", "MOD-003", "MOD-004", "MOD-006", "PRE-005", "PRE-006"))
            self._check_layers_structure(resolved_files, violations)
            self._check_forbidden_views(resolved_files, violations)
            self._check_pure_dart_domain(resolved_contents, violations)
            self._check_di_file(resolved_files, resolved_contents, violations)
            self._check_screens(resolved_files, resolved_contents, violations)
        else:
            # External layouts and DI are verified against Client source, not the company blueprint.
            for path in sorted(resolved_files):
                code = resolved_contents.get(path, "")
                if not code.strip():
                    continue
                layer = next((part for part in Path(path).parts[:-1] if part in {"domain", "data", "presentation"}), "module")
                result = architecture_validator.validate(code, layer, architecture_profile)
                if result["status"] == "error":
                    violations.append(ModuleViolation(
                        "MOD-007-SOURCE", "ERROR", path, None, result["error"], "Repair source and run the Client analyzer.",
                    ))
                    continue
                checked_rules.extend(result["checked_rules"])
                for finding in result["violations"]:
                    violations.append(ModuleViolation(
                        finding["rule_id"], finding["severity"], path, finding["line_number"],
                        finding["message"], finding["suggestion"],
                    ))

        has_errors = any(v.severity == "ERROR" for v in violations)
        has_warnings = any(v.severity == "WARNING" for v in violations)
        has_screens = any(path.startswith("presentation/screens/") for path in resolved_files)

        return {
            "status": "success",
            "feature_name": feature_name,
            "architecture_profile": architecture_profile,
            "gate_status": "FAILED" if has_errors else "UNVERIFIED" if has_warnings or has_screens or architecture_profile != "imespro" else "PASSED",
            "valid": not has_errors,
            "violations_count": len(violations),
            "errors_count": sum(1 for v in violations if v.severity == "ERROR"),
            "warnings_count": sum(1 for v in violations if v.severity == "WARNING"),
            "violations": [v.to_dict() for v in violations],
            "checked_rules": sorted(set(checked_rules)),
            "detected_files_count": len(resolved_files),
            "unsupported_checks": ([
                "Screen base import, registry, routing, tracking and responsive behavior require "
                "Client package resolution, analyzer and applicable runtime evidence."
            ] if has_screens else []) + ([
                "External module layout, foundation reuse, DI and files outside recognizable domain/data/presentation "
                "folders require Client inspection against the approved design. Dart syntax requires Client analysis."
            ] if architecture_profile != "imespro" else []),
        }

    def _check_screens(
        self,
        files: set[str],
        contents: dict[str, str],
        violations: list[ModuleViolation],
    ) -> None:
        """Check paths and clear local screen declarations, not runtime behavior."""
        for path in sorted(files):
            if not path.startswith("presentation/") or not path.endswith(".dart"):
                continue
            in_screens = path.startswith("presentation/screens/")
            if path.startswith("presentation/pages/"):
                violations.append(ModuleViolation(
                    "MOD-006-LEGACY-PAGE", "WARNING", path, None,
                    f"Legacy screen path '{path}' uses pages/ naming; scope is unverified.",
                    "Migrate only screens in the approved change; use presentation/screens/*_screen.dart for new work.",
                ))
            elif in_screens and not path.endswith("_screen.dart"):
                violations.append(ModuleViolation(
                    "MOD-006-SCREEN-PATH", "ERROR", path, None,
                    f"Screen file '{path}' must end in _screen.dart.",
                    "Name screen files *_screen.dart; place dialogs and child widgets under widgets/.",
                ))

            code = contents.get(path, "")
            if not code.strip():
                continue  # MOD-005 already records missing source.
            classes = _class_blocks(strip_comments_and_strings(code))
            screen_classes = [
                block for block in classes
                if not block.is_abstract and block.name not in {"BaseScreen", "BaseScreenState"}
                and block.superclass not in NON_WIDGET_SCREEN_SUPERCLASSES
                and (block.superclass == "BaseScreen" or (
                    block.name.endswith(("Screen", "Page"))
                    and block.superclass is not None
                ))
            ]
            if in_screens and not screen_classes:
                violations.append(ModuleViolation(
                    "MOD-006-MISSING-SCREEN", "ERROR", path, None,
                    f"Screen file '{path}' has no identifiable screen widget class.",
                    "Declare the routed *Screen widget and verify its active BaseScreen contract.",
                ))
            if screen_classes and not in_screens and not path.startswith("presentation/pages/"):
                violations.append(ModuleViolation(
                    "MOD-006-SCREEN-PATH", "ERROR", path, None,
                    f"Screen widget in '{path}' must be under presentation/screens/.",
                    "Move the screen into presentation/screens/*_screen.dart with its routes/imports.",
                ))
            if not (screen_classes or in_screens or path.startswith("presentation/pages/")):
                continue
            result = architecture_validator.validate(code, "presentation")
            if result["status"] == "error":
                violations.append(ModuleViolation(
                    "MOD-007-SCREEN-SOURCE", "WARNING", path, None,
                    f"Screen source could not be inspected: {result['error']}",
                    "Repair source and run the Client analyzer before approving the screen.",
                ))
                continue
            for finding in result["violations"]:
                if finding["rule_id"] in {"PRE-005", "PRE-006"}:
                    violations.append(ModuleViolation(
                        finding["rule_id"],
                        "WARNING" if path.startswith("presentation/pages/") else finding["severity"], path,
                        finding["line_number"], finding["message"], finding["suggestion"],
                    ))

    def _check_layers_structure(
        self,
        files: set[str],
        violations: list[ModuleViolation],
    ) -> None:
        """Verify presence of domain/, data/, presentation/ and di.dart."""
        has_domain = any(f.startswith("domain/") for f in files)
        has_data = any(f.startswith("data/") for f in files)
        has_presentation = any(f.startswith("presentation/") for f in files)
        has_di = "di.dart" in files

        if not has_domain:
            violations.append(
                ModuleViolation(
                    rule_id="MOD-001-MISSING-DOMAIN",
                    severity="ERROR",
                    file_path="domain/",
                    line_number=None,
                    message="Missing 'domain/' layer. Module must have domain/entities, domain/repo, and domain/usecases.",
                    suggestion="Create domain layer with pure Dart business entities, repository contracts, and use cases.",
                )
            )

        if not has_data:
            violations.append(
                ModuleViolation(
                    rule_id="MOD-001-MISSING-DATA",
                    severity="ERROR",
                    file_path="data/",
                    line_number=None,
                    message="Missing 'data/' layer. Module must have data/data_sources, data/models, data/mappers, and data/repo_impl.",
                    suggestion="Create data layer with BaseDataSource, safe JSON models, mappers, and repository implementations.",
                )
            )

        if not has_presentation:
            violations.append(
                ModuleViolation(
                    rule_id="MOD-001-MISSING-PRESENTATION",
                    severity="ERROR",
                    file_path="presentation/",
                    line_number=None,
                    message="Missing 'presentation/' layer. Module must have presentation/bloc, presentation/screens, and presentation/widgets.",
                    suggestion="Create presentation layer with Cubits (Pattern A BaseBlocState), screens, and widgets.",
                )
            )

        if not has_di:
            violations.append(
                ModuleViolation(
                    rule_id="MOD-001-MISSING-DI",
                    severity="ERROR",
                    file_path="di.dart",
                    line_number=None,
                    message="Missing 'di.dart' at module root.",
                    suggestion="Create 'di.dart' registering dependencies in 5 steps (Mapper -> DataSource -> Repo -> UseCase -> Cubit).",
                )
            )

    def _check_forbidden_views(
        self,
        files: set[str],
        violations: list[ModuleViolation],
    ) -> None:
        """Disallow unstructured 'views/' directories directly under the module."""
        forbidden_views = [f for f in files if f.startswith("views/")]
        if forbidden_views:
            violations.append(
                ModuleViolation(
                    rule_id="MOD-002-FORBIDDEN-VIEWS-DIR",
                    severity="ERROR",
                    file_path="views/",
                    line_number=None,
                    message=(
                        f"Found forbidden horizontal 'views/' directory with {len(forbidden_views)} files. "
                        "In Clean Architecture, screens must be under 'presentation/screens/' and widgets under 'presentation/widgets/'."
                    ),
                    suggestion="Move files from 'views/' to 'presentation/screens/' and 'presentation/widgets/'.",
                )
            )

    def _check_pure_dart_domain(
        self,
        contents: dict[str, str],
        violations: list[ModuleViolation],
    ) -> None:
        """Ensure no domain file imports package:flutter/."""
        flutter_pattern = re.compile(r"^\s*(?:import|export)\s+['\"]package:flutter/", re.MULTILINE)

        for path, code in contents.items():
            if path.startswith("domain/"):
                for idx, line in enumerate(code.splitlines(), start=1):
                    if flutter_pattern.search(line):
                        violations.append(
                            ModuleViolation(
                                rule_id="MOD-003-DOMAIN-FLUTTER-IMPORT",
                                severity="ERROR",
                                file_path=path,
                                line_number=idx,
                                message=f"Domain file '{path}' imports Flutter framework ('package:flutter/...'). Domain must remain pure Dart.",
                                suggestion="Remove Flutter imports from domain layer. Move UI or Widget dependencies to presentation layer.",
                            )
                        )

    def _check_di_file(
        self,
        files: set[str],
        contents: dict[str, str],
        violations: list[ModuleViolation],
    ) -> None:
        """Inspect di.dart to check 5-step registration order."""
        if "di.dart" not in files:
            return

        di_code = contents.get("di.dart", "")
        if not di_code:
            return

        has_mapper = bool(re.search(r"register(?:Lazy)?Singleton.*?\b\w+Mapper\(", di_code))
        has_datasource = bool(re.search(r"register(?:Lazy)?Singleton.*?\b\w+DataSource\(", di_code))
        has_repo = bool(re.search(r"register(?:Lazy)?Singleton.*?<\s*\w+Repository\s*>.*?\b\w+Repo(?:sitory)?Impl\(", di_code))
        has_usecase = bool(re.search(r"register(?:Lazy)?Singleton.*?\b\w+UseCase\(", di_code))
        has_cubit = bool(re.search(r"registerFactory.*?\b\w+Cubit\(", di_code))

        missing_steps = []
        if not has_mapper:
            missing_steps.append("1. Mapper")
        if not has_datasource:
            missing_steps.append("2. DataSource")
        if not has_repo:
            missing_steps.append("3. Repository Contract & Impl")
        if not has_usecase:
            missing_steps.append("4. UseCase")
        if not has_cubit:
            missing_steps.append("5. Cubit")

        if missing_steps:
            violations.append(
                ModuleViolation(
                    rule_id="MOD-004-INCOMPLETE-DI-REGISTRATION",
                    severity="WARNING",
                    file_path="di.dart",
                    line_number=None,
                    message=f"di.dart is missing required 5-step registrations: {', '.join(missing_steps)}.",
                    suggestion=(
                        "Register module dependencies in 5 steps:\n"
                        "1. Mapper (registerLazySingleton)\n"
                        "2. DataSource (registerLazySingleton)\n"
                        "3. Repository<Contract>(RepoImpl) (registerLazySingleton)\n"
                        "4. UseCases (registerLazySingleton)\n"
                        "5. Cubits (registerFactory)"
                    ),
                )
            )


# Global singleton instance
module_architecture_validator = ModuleArchitectureValidator()
