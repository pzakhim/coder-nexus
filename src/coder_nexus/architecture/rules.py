"""Clean Architecture Rule Catalog and specifications.

Defines rules, severity levels, violation details, and references
for Domain, Data, Presentation, Core, and Style layers.
"""

from dataclasses import dataclass
from typing import Any, Literal


Severity = Literal["ERROR", "WARNING", "INFO"]


@dataclass(frozen=True)
class RuleDefinition:
    """Definition of an architectural validation rule."""

    rule_id: str
    name: str
    layer: str
    severity: Severity
    description: str
    source_reference: str
    suggestion: str


@dataclass
class RuleViolation:
    """A detected architectural violation."""

    rule_id: str
    severity: Severity
    line_number: int
    message: str
    suggestion: str

    def to_dict(self) -> dict[str, Any]:
        result = {
            "rule_id": self.rule_id,
            "severity": self.severity,
            "line_number": self.line_number,
            "message": self.message,
            "suggestion": self.suggestion,
        }
        definition = RULE_CATALOG.get(self.rule_id)
        if definition:
            result["source_reference"] = definition.source_reference
        return result


# Canonical Rule Catalog
RULE_CATALOG: dict[str, RuleDefinition] = {
    "DOM-001": RuleDefinition(
        rule_id="DOM-001",
        name="Domain No Flutter Imports",
        layer="domain",
        severity="ERROR",
        description="Domain layer must be pure Dart and must not import or export 'package:flutter/...'.",
        source_reference="plugins/coder-nexus-fe/rules/clean_architecture_rules.md §1 Domain Layer @2026-10-20",
        suggestion="Remove Flutter imports from Domain. Use pure Dart entities and types.",
    ),
    "DOM-002": RuleDefinition(
        rule_id="DOM-002",
        name="Domain No Data/Presentation Imports",
        layer="domain",
        severity="ERROR",
        description="Domain layer must not depend on Data (models/datasources) or Presentation layers.",
        source_reference="plugins/coder-nexus-fe/rules/clean_architecture_rules.md §1 Domain Layer @2026-10-20",
        suggestion="Keep Domain independent; define abstract contracts that Data implements.",
    ),
    "DOM-003": RuleDefinition(
        rule_id="DOM-003",
        name="Entity Immutability",
        layer="domain",
        severity="WARNING",
        description="Entity classes should have immutable final fields and implement equality.",
        source_reference="plugins/coder-nexus-fe/rules/clean_architecture_rules.md §1 Domain Layer @2026-10-20",
        suggestion="Declare Entity fields as 'final'; use the Client's existing value-equality convention.",
    ),
    "DAT-001": RuleDefinition(
        rule_id="DAT-001",
        name="DataSource Extends BaseDataSource",
        layer="data",
        severity="ERROR",
        description="Data source implementation must extend 'BaseDataSource'.",
        source_reference="plugins/coder-nexus-fe/rules/clean_architecture_rules.md §1 Data Layer @2026-10-20",
        suggestion="Ensure the DataSource class extends BaseDataSource: 'class ... extends BaseDataSource'.",
    ),
    "DAT-002": RuleDefinition(
        rule_id="DAT-002",
        name="Repo TryCatch & DataState",
        layer="data",
        severity="ERROR",
        description="Repository implementations must wrap API calls with tryCatch/tryCatchAsync and return DataState<T>.",
        source_reference="plugins/coder-nexus-fe/rules/clean_architecture_rules.md §1 Data Layer @2026-10-20",
        suggestion="Return DataState<T> and use the existing dataSource.method().tryCatch()/tryCatchAsync() extension.",
    ),
    "DAT-003": RuleDefinition(
        rule_id="DAT-003",
        name="Safe DTO Parsing",
        layer="data",
        severity="WARNING",
        description="DTO Model parsing should use safe helper utilities (e.g. parse_util) instead of unsafe raw casts.",
        source_reference="plugins/coder-nexus-fe/rules/clean_architecture_rules.md §1 Data Layer @2026-10-20",
        suggestion="Validate required fields and types explicitly or use the Client's verified safe parser helpers.",
    ),
    "PRE-001": RuleDefinition(
        rule_id="PRE-001",
        name="No Throw In Presentation",
        layer="presentation",
        severity="ERROR",
        description="Presentation layer must never throw exceptions or errors directly.",
        source_reference="plugins/coder-nexus-fe/rules/clean_architecture_rules.md §1 Presentation Layer @2026-10-20",
        suggestion="Emit error states in Cubit/BLoC or show user feedback dialog/toast instead of throwing.",
    ),
    "PRE-002": RuleDefinition(
        rule_id="PRE-002",
        name="State Extends BaseBlocState",
        layer="presentation",
        severity="WARNING",
        description="BLoC/Cubit state classes for new features should follow Pattern A and extend 'BaseBlocState'.",
        source_reference="plugins/coder-nexus-fe/rules/clean_architecture_rules.md §1 Presentation Layer @2026-10-20",
        suggestion="Extend BaseBlocState for standardized state tracking, status, and equatable props.",
    ),
    "PRE-003": RuleDefinition(
        rule_id="PRE-003",
        name="Resource Disposal In State",
        layer="presentation",
        severity="WARNING",
        description="StatefulWidget instantiating controllers or focus nodes must release them in dispose().",
        source_reference="plugins/coder-nexus-fe/skills/flutter/code-review/SKILL.md @2026-10-20",
        suggestion="Override dispose() and call controller.dispose() / super.dispose().",
    ),
    "PRE-004": RuleDefinition(
        rule_id="PRE-004",
        name="Prefer app_ui_kit Components",
        layer="presentation",
        severity="INFO",
        description="Prefer app_ui_kit components over raw primitive widgets when a GUIDE row fits.",
        source_reference="plugins/coder-nexus-fe/rules/clean_architecture_rules.md §4 Evidence, UI reuse, and code quality @2026-10-20",
        suggestion="Consider AppButton, AppFormField, or AppLoadingIndicator from app_ui_kit (see its GUIDE).",
    ),
    "PRE-005": RuleDefinition(
        rule_id="PRE-005",
        name="Screen Naming",
        layer="presentation",
        severity="ERROR",
        description="Screen destinations use a *Screen class, not *Page.",
        source_reference="plugins/coder-nexus-fe/skills/flutter/clean-architecture/references/05_screen_contract.md @2026-10-08",
        suggestion="Name the destination *Screen; update its file, routes, imports and tests together.",
    ),
    "PRE-006": RuleDefinition(
        rule_id="PRE-006",
        name="BaseScreen Contract",
        layer="presentation",
        severity="ERROR",
        description="A screen uses the active Client BaseScreen/BaseScreenState and metadata hook.",
        source_reference="plugins/coder-nexus-fe/skills/flutter/clean-architecture/references/05_screen_contract.md @2026-10-08",
        suggestion="Resolve the Client's active base API; missing or commented source is BLOCKED.",
    ),
    "DIR-001": RuleDefinition(
        rule_id="DIR-001",
        name="DI Cubit Factory Scope",
        layer="module",
        severity="WARNING",
        description="Screen-scoped Cubits should be registered as factory in GetIt, not as singletons.",
        source_reference="plugins/coder-nexus-fe/rules/clean_architecture_rules.md §2 Module DI Order @2026-10-20",
        suggestion="Use 'injector.registerFactory(() => ...Cubit(...))' for screen-scoped state management.",
    ),
    "STY-001": RuleDefinition(
        rule_id="STY-001",
        name="AppLogger Over Raw Print",
        layer="all",
        severity="WARNING",
        description="Avoid using raw 'print()' in production code. Use centralized 'AppLogger'.",
        source_reference="plugins/coder-nexus-fe/rules/clean_architecture_rules.md §4 Evidence, UI reuse, and code quality @2026-10-20",
        suggestion="Replace 'print(...)' with 'AppLogger.info(...)', 'AppLogger.error(...)', or appropriate level.",
    ),
    "RTE-001": RuleDefinition(
        rule_id="RTE-001",
        name="Route Annotation Contract",
        layer="presentation",
        severity="INFO",
        description="Screen classes should be annotated with '@RoutePage()' for auto_route generation.",
        source_reference="plugins/coder-nexus-fe/skills/flutter/clean-architecture/references/05_screen_contract.md @2026-10-20",
        suggestion="Add '@RoutePage()' annotation above the screen class declaration.",
    ),
}
