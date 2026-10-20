"""Architecture knowledge and structure package for Coder Nexus."""

from .module_validator import ModuleArchitectureValidator, module_architecture_validator
from .rules import RULE_CATALOG, RuleDefinition, RuleViolation
from .spec_validator import SpecValidator, spec_validator
from .structure import get_project_structure_data
from .validator import ArchitectureValidator, architecture_validator, strip_comments_and_strings

__all__ = [
    "RULE_CATALOG",
    "ArchitectureValidator",
    "ModuleArchitectureValidator",
    "RuleDefinition",
    "RuleViolation",
    "SpecValidator",
    "architecture_validator",
    "get_project_structure_data",
    "module_architecture_validator",
    "spec_validator",
    "strip_comments_and_strings",
]
