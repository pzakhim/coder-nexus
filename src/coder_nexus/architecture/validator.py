"""ArchitectureValidator engine for Clean Architecture code inspection.

Performs static lexical analysis and rule checking for Dart source code
per architectural layer without requiring external native dependencies.
Preserves line numbers accurately by stripping comments and strings with whitespace.
"""

import re
from dataclasses import dataclass
from typing import Any

from .rules import RULE_CATALOG, RuleViolation

# Lexer regex matching comments, import/export directives, and strings in Dart source.
# Note: comments are matched FIRST, then import/export directives (which must preserve their URI string),
# then general string literals.
_DART_LEX_REGEX = re.compile(
    r"(?P<comment_single>//[^\n]*)"
    r"|(?P<comment_multi>/\*[\s\S]*?\*/)"
    r"|(?P<import_directive>^[ \t]*(?:import|export|part)[ \t]+(?:['\"][^'\n]*['\"]|r['\"][^'\n]*['\"]))"
    r"|(?P<raw_triple_double>r\"\"\"[\s\S]*?\"\"\")"
    r"|(?P<raw_triple_single>r\'\'\'[\s\S]*?\'\'\')"
    r"|(?P<triple_double>\"\"\"[\s\S]*?\"\"\")"
    r"|(?P<triple_single>\'\'\'[\s\S]*?\'\'\')"
    r"|(?P<raw_string_double>r\"[^\"\n]*\")"
    r"|(?P<raw_string_single>r\'[^\'\n]*\')"
    r"|(?P<string_double>\"([^\"\\\n]|\\.)*\")"
    r"|(?P<string_single>\'([^\'\\\n]|\\.)*\')",
    re.MULTILINE,
)

VALID_LAYERS = {"domain", "data", "presentation", "core", "module"}
ARCHITECTURE_PROFILES = {"imespro", "external-structured", "external-standard"}
IMESPRO_ONLY_RULES = {"DAT-001", "DAT-002", "PRE-002", "PRE-004", "PRE-005", "PRE-006", "STY-001"}
NON_WIDGET_SCREEN_SUPERCLASSES = {"Equatable", "Object", "Page", "ScreenModel"}


def strip_comments_and_strings(code: str, preserve_directives: bool = True) -> str:
    """Mask comments and string literals with spaces while preserving line breaks.

    Import and export directives are kept intact so architectural boundary checks
    can inspect import paths. Comments and normal string literals are masked with spaces
    to prevent false-positives while keeping exact 1-to-1 line number alignment.
    """

    def _mask(m: re.Match[str]) -> str:
        # If it's an import or export directive, preserve it as-is
        if preserve_directives and m.group("import_directive"):
            return m.group(0)

        # Otherwise mask with spaces, preserving newlines
        text = m.group(0)
        return "".join("\n" if ch == "\n" else " " for ch in text)

    return _DART_LEX_REGEX.sub(_mask, code)


@dataclass(frozen=True)
class _ClassBlock:
    name: str
    superclass: str | None
    is_abstract: bool
    start: int
    body_start: int
    end: int
    body: str

    def line_number(self, code: str, offset: int = 0) -> int:
        return code[: self.body_start + offset].count("\n") + 1


_CLASS_PATTERN = re.compile(
    r"^[ \t]*(?P<modifiers>(?:(?:abstract|base|final|interface|sealed)\s+)*)"
    r"class\s+(?P<name>\w+)(?:\s*<[^>{}]*>)?"
    r"(?:\s+extends\s+(?P<superclass>\w+(?:\.\w+)?)(?:\s*<[^>{}]*>)?)?[^;{}]*\{",
    re.MULTILINE,
)


def _class_blocks(code: str) -> list[_ClassBlock]:
    """Return top-level class bodies from already-masked Dart source."""
    blocks: list[_ClassBlock] = []
    for match in _CLASS_PATTERN.finditer(code):
        body_start = match.end() - 1
        depth = 0
        body_end = len(code)
        for index in range(body_start, len(code)):
            if code[index] == "{":
                depth += 1
            elif code[index] == "}":
                depth -= 1
                if depth == 0:
                    body_end = index
                    break
        blocks.append(
            _ClassBlock(
                name=match.group("name"),
                superclass=match.group("superclass").split(".")[-1] if match.group("superclass") else None,
                is_abstract="abstract" in match.group("modifiers").split(),
                start=match.start(),
                body_start=body_start + 1,
                end=body_end + 1,
                body=code[body_start + 1 : body_end],
            )
        )
    return blocks


def _unbalanced_delimiter(code: str) -> tuple[str, int] | None:
    """Find clear delimiter errors without pretending to parse Dart syntax."""
    masked = strip_comments_and_strings(code, preserve_directives=False)
    opening_for = {")": "(", "]": "[", "}": "{"}
    stack: list[tuple[str, int]] = []
    for index, char in enumerate(masked):
        if char in "([{":
            stack.append((char, index))
        elif char in ")]}" and (not stack or stack[-1][0] != opening_for[char]):
            return char, masked[:index].count("\n") + 1
        elif char in ")]}":
            stack.pop()
    if stack:
        char, index = stack[-1]
        return char, masked[:index].count("\n") + 1
    return None


class ArchitectureValidator:
    """Validator engine verifying Clean Architecture rules on Dart source code."""

    def validate(self, dart_code: str, layer: str, architecture_profile: str = "imespro") -> dict[str, Any]:
        """Validate Dart source code against architectural rules for a specified layer.

        Args:
            dart_code: The Dart source code to analyze.
            layer: One of 'domain', 'data', 'presentation', 'core', 'module'.
            architecture_profile: Approved foundation profile; defaults to legacy iMESPro checks.

        Returns:
            Dictionary containing validation status, violations, and unsupported checks.
        """
        if architecture_profile not in ARCHITECTURE_PROFILES:
            return {"status": "error", "error": f"Unknown architecture_profile: {architecture_profile!r}."}
        clean_code = dart_code if dart_code is not None else ""
        if not clean_code.strip():
            return {
                "status": "error",
                "error": "dart_code cannot be empty.",
            }

        clean_layer = (layer or "").strip().lower()
        if clean_layer not in VALID_LAYERS:
            return {
                "status": "error",
                "error": (
                    f"Invalid layer '{layer}'. Supported layers are: "
                    f"{', '.join(sorted(VALID_LAYERS))}."
                ),
            }

        delimiter_error = _unbalanced_delimiter(clean_code)
        if delimiter_error:
            delimiter, line_number = delimiter_error
            return {
                "status": "error",
                "syntax_status": "INVALID",
                "error": f"Unbalanced Dart delimiter '{delimiter}' at line {line_number}.",
            }

        stripped_code = strip_comments_and_strings(clean_code)
        lines = stripped_code.splitlines()

        violations: list[RuleViolation] = []
        checked_rules: list[str] = []
        unsupported_checks: list[str] = [
            "Dart syntax: NOT_CHECKED by the lexical Hub validator; Client analyzer evidence is required."
        ]

        # 1. Global / Style checks (all layers)
        self._check_style_rules(lines, violations, checked_rules)

        # 2. Layer-specific checks
        if clean_layer == "domain":
            self._check_domain_rules(lines, stripped_code, violations, checked_rules)
            unsupported_checks.append(
                "DOM-002: Transitive package export resolution requires Client workspace analysis."
            )
        elif clean_layer == "data":
            self._check_data_rules(lines, stripped_code, violations, checked_rules)
            unsupported_checks.extend([
                "DAT-001: Verification of indirect BaseDataSource inheritance via custom base "
                "classes requires Client workspace.",
                "DAT-002: Runtime API error serialization verification requires integration tests.",
            ])
        elif clean_layer == "presentation":
            self._check_presentation_rules(lines, stripped_code, violations, checked_rules)
            unsupported_checks.extend([
                "PRE-003: Runtime memory leak detection and Cubit stream unsubscription requires runtime profiling.",
                "PRE-004: Semantic token matching against Figma tokens requires live design sync.",
                "PRE-005: File and folder naming requires the module path; source-only validation checks class names.",
                "PRE-006: Lexical declarations do not prove Client package resolution, inherited behavior, "
                "router integration, tracking events or responsive layouts. Inspect and run the Client.",
            ])
        elif clean_layer in ("core", "module"):
            self._check_di_rules(
                stripped_code,
                checked_rules,
                unsupported_checks,
            )
            unsupported_checks.append(
                "DIR-001: Resolution of cross-module circular DI dependencies requires full "
                "modules_di.dart inspection at Client."
            )

        if architecture_profile != "imespro":
            # Company conventions are not evidence of a defect in an external Client.
            violations = [v for v in violations if v.rule_id not in IMESPRO_ONLY_RULES]
            checked_rules = [rule for rule in checked_rules if rule not in IMESPRO_ONLY_RULES]
            unsupported_checks = [
                check for check in unsupported_checks
                if check.split(":", 1)[0] not in IMESPRO_ONLY_RULES | {"DIR-001"}
            ]
            unsupported_checks.append(
                "Client foundation, screen naming/base, state, error handling and DI conventions require "
                "inspection against the approved design and resolved Client source."
            )

        # Sort violations by line number
        violations.sort(key=lambda v: v.line_number)

        # Code is valid if there are no ERROR severity violations
        has_errors = any(v.severity == "ERROR" for v in violations)

        return {
            "status": "success",
            "analysis_kind": "lexical",
            "syntax_status": "NOT_CHECKED",
            "gate_status": "FAILED" if has_errors else "UNVERIFIED",
            "layer": clean_layer,
            "architecture_profile": architecture_profile,
            "valid": not has_errors,
            "violations_count": len(violations),
            "errors_count": sum(1 for v in violations if v.severity == "ERROR"),
            "warnings_count": sum(1 for v in violations if v.severity == "WARNING"),
            "violations": [v.to_dict() for v in violations],
            "checked_rules": sorted(list(set(checked_rules))),
            "unsupported_checks": unsupported_checks,
        }

    def _check_style_rules(
        self,
        lines: list[str],
        violations: list[RuleViolation],
        checked_rules: list[str],
    ) -> None:
        """Check style rules (STY-001) across all layers."""
        checked_rules.append("STY-001")
        rule = RULE_CATALOG["STY-001"]
        print_pattern = re.compile(r"\b(print|debugPrint)\s*\(")

        for idx, line in enumerate(lines, start=1):
            if print_pattern.search(line):
                violations.append(
                    RuleViolation(
                        rule_id=rule.rule_id,
                        severity=rule.severity,
                        line_number=idx,
                        message="Direct 'print()' or 'debugPrint()' detected. Use 'AppLogger' instead.",
                        suggestion=rule.suggestion,
                    )
                )

    def _check_domain_rules(
        self,
        lines: list[str],
        stripped_code: str,
        violations: list[RuleViolation],
        checked_rules: list[str],
    ) -> None:
        """Check rules for domain layer (DOM-001, DOM-002, DOM-003)."""
        # DOM-001: No Flutter imports
        checked_rules.append("DOM-001")
        dom_001 = RULE_CATALOG["DOM-001"]
        flutter_import_pattern = re.compile(r"^\s*(?:import|export)\s+['\"]package:flutter/")

        for idx, line in enumerate(lines, start=1):
            if flutter_import_pattern.search(line):
                violations.append(
                    RuleViolation(
                        rule_id=dom_001.rule_id,
                        severity=dom_001.severity,
                        line_number=idx,
                        message=(
                            "Domain layer must not import or export Flutter framework "
                            "('package:flutter/...'). Domain must remain pure Dart."
                        ),
                        suggestion=dom_001.suggestion,
                    )
                )

        # DOM-002: No Data or Presentation imports
        checked_rules.append("DOM-002")
        dom_002 = RULE_CATALOG["DOM-002"]
        data_pres_pattern = re.compile(
            r"^\s*(?:import|export)\s+['\"][^'\"]*(/data/|/presentation/|\.\./data/|\.\./presentation/)"
        )

        for idx, line in enumerate(lines, start=1):
            if data_pres_pattern.search(line):
                violations.append(
                    RuleViolation(
                        rule_id=dom_002.rule_id,
                        severity=dom_002.severity,
                        line_number=idx,
                        message="Domain layer must not import Data or Presentation layers.",
                        suggestion=dom_002.suggestion,
                    )
                )

        # DOM-003: Entity Immutability
        checked_rules.append("DOM-003")
        dom_003 = RULE_CATALOG["DOM-003"]
        mutable_field_pattern = re.compile(
            r"^\s*(?:late\s+)?(?:var|[A-Za-z_]\w*(?:\s*<[^;=]+>)?\??)"
            r"\s+\w+\s*(?:=[^;]*)?;",
            re.MULTILINE,
        )

        for block in _class_blocks(stripped_code):
            if not block.name.endswith("Entity"):
                continue
            for match in mutable_field_pattern.finditer(block.body):
                declaration = match.group(0).lstrip()
                if declaration.startswith(("final ", "const ", "static ", "late final ")):
                    continue
                violations.append(
                    RuleViolation(
                        rule_id=dom_003.rule_id,
                        severity=dom_003.severity,
                        line_number=block.line_number(stripped_code, match.start()),
                        message="Entity fields should be immutable ('final'). Mutable field detected in Entity.",
                        suggestion=dom_003.suggestion,
                    )
                )

    def _check_data_rules(
        self,
        lines: list[str],
        stripped_code: str,
        violations: list[RuleViolation],
        checked_rules: list[str],
    ) -> None:
        """Check rules for data layer (DAT-001, DAT-002, DAT-003)."""
        # DAT-001: DataSource extends BaseDataSource
        checked_rules.append("DAT-001")
        dat_001 = RULE_CATALOG["DAT-001"]
        class_blocks = _class_blocks(stripped_code)
        for block in class_blocks:
            if block.is_abstract or not re.search(r"DataSource(?:Impl)?$", block.name):
                continue
            if block.superclass is None:
                violations.append(
                    RuleViolation(
                        rule_id=dat_001.rule_id,
                        severity=dat_001.severity,
                        line_number=stripped_code[: block.start].count("\n") + 1,
                        message=f"DataSource class '{block.name}' must extend 'BaseDataSource' (found: 'none').",
                        suggestion=dat_001.suggestion,
                    )
                )
            elif block.superclass != "BaseDataSource":
                violations.append(
                    RuleViolation(
                        rule_id=dat_001.rule_id,
                        severity="WARNING",
                        line_number=stripped_code[: block.start].count("\n") + 1,
                        message=(
                            f"DataSource class '{block.name}' extends '{block.superclass}'. "
                            "Indirect BaseDataSource inheritance requires Client workspace resolution."
                        ),
                        suggestion="Resolve the inheritance chain before deciding whether a change is required.",
                    )
                )

        # DAT-002: Repository implementation returns DataState & wraps tryCatch
        checked_rules.append("DAT-002")
        dat_002 = RULE_CATALOG["DAT-002"]
        repository_method_pattern = re.compile(
            r"^[ \t]*(?:@override[ \t]*\n[ \t]*)?"
            r"(?P<return>Future\s*<[^;\n{=]+>|DataState\s*<[^;\n{=]+>)"
            r"\s+(?P<name>[A-Za-z]\w*)\s*\([^;{}]*\)\s*(?:async\s*)?(?:\{|=>)",
            re.MULTILINE,
        )
        for block in class_blocks:
            if not re.search(r"Repo(?:sitory)?Impl$", block.name):
                continue
            method_matches = list(repository_method_pattern.finditer(block.body))
            if not method_matches:
                violations.append(
                    RuleViolation(
                        rule_id=dat_002.rule_id,
                        severity=dat_002.severity,
                        line_number=stripped_code[: block.start].count("\n") + 1,
                        message=f"Repository implementation '{block.name}' has no verifiable DataState method contract.",
                        suggestion=dat_002.suggestion,
                    )
                )
                continue
            for index, method in enumerate(method_matches):
                segment_end = (
                    method_matches[index + 1].start()
                    if index + 1 < len(method_matches)
                    else len(block.body)
                )
                method_text = block.body[method.start() : segment_end]
                returns_data_state = "DataState" in method.group("return")
                wraps_error = re.search(
                    r"(?:\.|\b)tryCatch(?:Async)?(?:\s*<[^>]+>)?\s*\(",
                    method_text,
                )
                if returns_data_state and wraps_error:
                    continue
                violations.append(
                    RuleViolation(
                        rule_id=dat_002.rule_id,
                        severity=dat_002.severity,
                        line_number=block.line_number(stripped_code, method.start()),
                        message=(
                            f"Repository method '{method.group('name')}' must return DataState<T> "
                            "and handle the call with tryCatch/tryCatchAsync."
                        ),
                        suggestion=dat_002.suggestion,
                    )
                )

        # DAT-003: Safe DTO Parsing (avoid raw casts like 'as String')
        checked_rules.append("DAT-003")
        dat_003 = RULE_CATALOG["DAT-003"]
        model_class_pattern = re.compile(r"\bclass\s+(\w+Model)\b")
        unsafe_cast_pattern = re.compile(r"\bas\s+(String|int|double|bool|num)\b")

        if model_class_pattern.search(stripped_code):
            for idx, line in enumerate(lines, start=1):
                if unsafe_cast_pattern.search(line):
                    violations.append(
                        RuleViolation(
                            rule_id=dat_003.rule_id,
                            severity=dat_003.severity,
                            line_number=idx,
                            message="DTO model parsing uses unsafe raw cast ('as Type'). Prefer safe parse helpers.",
                            suggestion=dat_003.suggestion,
                        )
                    )

    def _check_presentation_rules(
        self,
        lines: list[str],
        stripped_code: str,
        violations: list[RuleViolation],
        checked_rules: list[str],
    ) -> None:
        """Check rules for presentation layer (PRE-001, PRE-002, PRE-003, PRE-004, RTE-001)."""
        # PRE-001: Never throw in Presentation
        checked_rules.append("PRE-001")
        pre_001 = RULE_CATALOG["PRE-001"]
        throw_pattern = re.compile(r"\bthrow\s+")

        for idx, line in enumerate(lines, start=1):
            if throw_pattern.search(line):
                violations.append(
                    RuleViolation(
                        rule_id=pre_001.rule_id,
                        severity=pre_001.severity,
                        line_number=idx,
                        message="Presentation layer must never throw exceptions or errors directly.",
                        suggestion=pre_001.suggestion,
                    )
                )

        # PRE-002: State extends BaseBlocState
        checked_rules.append("PRE-002")
        pre_002 = RULE_CATALOG["PRE-002"]
        # Match class ending with State that is not a StatefulWidget State<_WidgetState extends State<Widget>>
        class_blocks = _class_blocks(stripped_code)
        state_supers = {
            block.name: block.superclass
            for block in class_blocks
            if block.name.endswith("State")
        }

        def follows_supported_state_pattern(class_name: str) -> bool:
            visited: set[str] = set()
            current = class_name
            while current not in visited:
                visited.add(current)
                superclass = state_supers.get(current)
                if superclass in {"BaseBlocState", "Equatable"}:
                    return True
                if superclass not in state_supers:
                    return False
                current = superclass
            return False

        for block in class_blocks:
            if not block.name.endswith("State"):
                continue
            if block.superclass in {"State", "BaseScreenState"} or block.name.startswith("_"):
                continue
            if not follows_supported_state_pattern(block.name):
                violations.append(
                    RuleViolation(
                        rule_id=pre_002.rule_id,
                        severity=pre_002.severity,
                        line_number=stripped_code[: block.start].count("\n") + 1,
                        message=(
                            f"BLoC/Cubit state '{block.name}' should follow a BaseBlocState or "
                            f"legacy Equatable hierarchy (found: '{block.superclass or 'none'}')."
                        ),
                        suggestion=pre_002.suggestion,
                    )
                )

        # PRE-003: Resource Disposal in StatefulWidget State
        checked_rules.append("PRE-003")
        pre_003 = RULE_CATALOG["PRE-003"]
        controller_pattern = re.compile(
            r"\b(TextEditingController|AnimationController|ScrollController|FocusNode)\s*\("
        )
        dispose_pattern = re.compile(r"\bvoid\s+dispose\s*\(\s*\)")
        owned_resource_pattern = re.compile(
            r"\b(?P<name>\w+)\s*=\s*"
            r"(?:TextEditingController|AnimationController|ScrollController|FocusNode)\s*\("
        )

        for block in class_blocks:
            if block.superclass not in {"State", "BaseScreenState"} or not controller_pattern.search(block.body):
                continue
            missing_dispose = not dispose_pattern.search(block.body)
            undisposed_resources = [
                match.group("name")
                for match in owned_resource_pattern.finditer(block.body)
                if not re.search(rf"\b{re.escape(match.group('name'))}\.dispose\s*\(", block.body)
            ]
            if missing_dispose or undisposed_resources:
                detail = (
                    "missing dispose()"
                    if missing_dispose
                    else f"resources not disposed: {', '.join(undisposed_resources)}"
                )
                violations.append(
                    RuleViolation(
                        rule_id=pre_003.rule_id,
                        severity=pre_003.severity,
                        line_number=stripped_code[: block.start].count("\n") + 1,
                        message=f"StatefulWidget State '{block.name}' owns resources but has {detail}.",
                        suggestion=pre_003.suggestion,
                    )
                )

        # PRE-004: Prefer App UI Kit components over primitive widgets
        checked_rules.append("PRE-004")
        pre_004 = RULE_CATALOG["PRE-004"]
        primitive_pattern = re.compile(
            r"\b(ElevatedButton|TextButton|TextField|CircularProgressIndicator)\s*\("
        )

        for idx, line in enumerate(lines, start=1):
            match = primitive_pattern.search(line)
            if match:
                widget_name = match.group(1)
                violations.append(
                    RuleViolation(
                        rule_id=pre_004.rule_id,
                        severity=pre_004.severity,
                        line_number=idx,
                        message=(
                            f"Raw primitive widget '{widget_name}' detected. Prefer standard "
                            "component from 'app_ui_kit'."
                        ),
                        suggestion=pre_004.suggestion,
                    )
                )

        self._check_screen_contract(stripped_code, class_blocks, violations, checked_rules)

        # RTE-001: Route annotation applies only when auto_route is imported.
        checked_rules.append("RTE-001")
        rte_001 = RULE_CATALOG["RTE-001"]
        uses_auto_route = bool(re.search(r"\bimport\s+['\"]package:auto_route/", stripped_code))
        previous_class_end = 0
        for block in class_blocks:
            if (uses_auto_route and block.name.endswith(("Screen", "Page"))
                    and not block.is_abstract and block.name != "BaseScreen"
                    and block.superclass not in NON_WIDGET_SCREEN_SUPERCLASSES):
                declaration_context = stripped_code[previous_class_end : block.start]
                if "@RoutePage" not in declaration_context:
                    violations.append(
                        RuleViolation(
                            rule_id=rte_001.rule_id,
                            severity=rte_001.severity,
                            line_number=stripped_code[: block.start].count("\n") + 1,
                            message=f"Screen class '{block.name}' is missing '@RoutePage()' annotation.",
                            suggestion=rte_001.suggestion,
                        )
                    )
            previous_class_end = max(previous_class_end, block.end)

    def _check_screen_contract(
        self,
        code: str,
        blocks: list[_ClassBlock],
        violations: list[RuleViolation],
        checked_rules: list[str],
    ) -> None:
        """Catch clear screen declaration defects without guessing UI ownership."""
        checked_rules.extend(("PRE-005", "PRE-006"))
        for block in blocks:
            if block.is_abstract or block.name in {"BaseScreen", "BaseScreenState"}:
                continue
            # A Page<T> route object is not a screen. Dialogs/sheets/child widgets
            # should have their own names and are classified from Client context.
            if not (block.superclass == "BaseScreen" or (
                block.name.endswith(("Screen", "Page")) and block.superclass is not None
            )):
                continue
            if block.superclass in NON_WIDGET_SCREEN_SUPERCLASSES:
                continue
            line = code[:block.start].count("\n") + 1
            if not block.name.endswith("Screen"):
                rule = RULE_CATALOG["PRE-005"]
                violations.append(RuleViolation(
                    rule.rule_id, rule.severity, line,
                    f"Screen widget '{block.name}' must use the *Screen suffix.", rule.suggestion,
                ))

            rule = RULE_CATALOG["PRE-006"]
            if block.superclass != "BaseScreen":
                definite = block.superclass in {"StatelessWidget", "StatefulWidget", "Widget"}
                severity = rule.severity if definite else "WARNING"
                violations.append(RuleViolation(
                    rule.rule_id, severity, line,
                    f"Screen '{block.name}' extends {block.superclass or 'an unknown parent'}; "
                    + ("use the active BaseScreen." if definite else
                       "indirect BaseScreen inheritance is UNVERIFIED in this file."),
                    rule.suggestion,
                ))
                continue

        for block in blocks:
            header = code[block.start:block.body_start]
            if block.superclass == "State" and re.search(
                r"\bState\s*<\s*\w+(?:Screen|Page)\s*>", header
            ):
                rule = RULE_CATALOG["PRE-006"]
                violations.append(RuleViolation(
                    rule.rule_id, rule.severity, code[:block.start].count("\n") + 1,
                    f"Screen state '{block.name}' extends State; use BaseScreenState.", rule.suggestion,
                ))

    def _check_di_rules(
        self,
        stripped_code: str,
        checked_rules: list[str],
        unsupported_checks: list[str],
    ) -> None:
        """Check rules for DI registrations (DIR-001)."""
        checked_rules.append("DIR-001")
        singleton_cubit_pattern = re.compile(
            r"injector\.register(?:Lazy)?Singleton\s*(?:<[^>]+>)?\s*\(\s*\(\s*\)\s*=>\s*(\w+Cubit)\("
        )

        for match in singleton_cubit_pattern.finditer(stripped_code):
            cubit_name = match.group(1)
            unsupported_checks.append(
                f"DIR-001: Cubit '{cubit_name}' uses singleton registration; lifetime is UNVERIFIED "
                "until Client callers confirm whether it is app-wide or screen-scoped."
            )


# Singleton validator instance
architecture_validator = ArchitectureValidator()
