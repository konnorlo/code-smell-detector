from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum


class SmellType(Enum):
    LONG_METHOD = "long_method"
    COMPLEX_CONDITIONAL = "complex_conditional"
    DUPLICATE_CODE = "duplicate_code"
    POOR_NAMING = "poor_naming"
    HIGH_COMPLEXITY = "high_complexity"
    TIGHT_COUPLING = "tight_coupling"
    DEAD_CODE = "dead_code"
    LARGE_CLASS = "large_class"
    FEATURE_ENVY = "feature_envy"
    DATA_CLUMPS = "data_clumps"


class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class CodeSmell:
    smell_type: SmellType
    severity: Severity
    line_start: int
    line_end: int
    column_start: int
    column_end: int
    message: str
    suggestion: str
    confidence: float
    file_path: str
    function_name: Optional[str] = None
    class_name: Optional[str] = None
    metrics: Dict[str, Any] = None

    def __post_init__(self):
        if self.metrics is None:
            self.metrics = {}


@dataclass
class FileAnalysis:
    file_path: str
    language: str
    lines_of_code: int
    smells: List[CodeSmell]
    metrics: Dict[str, Any]
    
    def __post_init__(self):
        if self.metrics is None:
            self.metrics = {}


@dataclass
class ProjectAnalysis:
    project_path: str
    files: List[FileAnalysis]
    summary: Dict[str, Any]
    total_smells: int
    
    def __post_init__(self):
        if self.summary is None:
            self.summary = {}
        self.total_smells = sum(len(file.smells) for file in self.files)


@dataclass
class CodeMetrics:
    cyclomatic_complexity: int
    lines_of_code: int
    cognitive_complexity: int
    nesting_depth: int
    parameter_count: int
    variable_count: int
    duplicate_lines: int
    maintainability_index: float
    halstead_difficulty: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'cyclomatic_complexity': self.cyclomatic_complexity,
            'lines_of_code': self.lines_of_code,
            'cognitive_complexity': self.cognitive_complexity,
            'nesting_depth': self.nesting_depth,
            'parameter_count': self.parameter_count,
            'variable_count': self.variable_count,
            'duplicate_lines': self.duplicate_lines,
            'maintainability_index': self.maintainability_index,
            'halstead_difficulty': self.halstead_difficulty
        }