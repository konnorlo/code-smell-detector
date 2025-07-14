from typing import List, Dict, Any
import ast
from pathlib import Path

from ..core.models import CodeSmell, SmellType, Severity, FileAnalysis
from ..parsers.base_parser import PythonParser


class SmellDetector:
    def __init__(self):
        self.parsers = {
            'python': PythonParser()
        }
        self.rules = [
            LongMethodRule(),
            ComplexConditionalRule(),
            HighComplexityRule(),
            PoorNamingRule(),
            LargeClassRule(),
            DeadCodeRule()
        ]
    
    def detect_smells(self, file_path: str) -> FileAnalysis:
        parser = self._get_parser(file_path)
        if not parser:
            return FileAnalysis(file_path, 'unknown', 0, [], {})
        
        analysis = parser.parse_file(file_path)
        
        content = parser.read_file(file_path)
        tree = ast.parse(content)
        
        for rule in self.rules:
            if rule.supports_language(analysis.language):
                smells = rule.detect(tree, file_path, content)
                analysis.smells.extend(smells)
        
        return analysis
    
    def _get_parser(self, file_path: str):
        for parser in self.parsers.values():
            if parser.can_parse(file_path):
                return parser
        return None


class SmellRule:
    def __init__(self):
        self.supported_languages = []
    
    def supports_language(self, language: str) -> bool:
        return language in self.supported_languages
    
    def detect(self, tree: ast.AST, file_path: str, content: str) -> List[CodeSmell]:
        raise NotImplementedError


class LongMethodRule(SmellRule):
    def __init__(self):
        super().__init__()
        self.supported_languages = ['python']
        self.max_lines = 30
    
    def detect(self, tree: ast.AST, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.end_lineno and node.lineno:
                    method_length = node.end_lineno - node.lineno
                    if method_length > self.max_lines:
                        severity = Severity.HIGH if method_length > 50 else Severity.MEDIUM
                        confidence = min(0.9, (method_length - self.max_lines) / self.max_lines)
                        
                        smells.append(CodeSmell(
                            smell_type=SmellType.LONG_METHOD,
                            severity=severity,
                            line_start=node.lineno,
                            line_end=node.end_lineno,
                            column_start=node.col_offset,
                            column_end=node.end_col_offset or 0,
                            message=f"Method '{node.name}' is too long ({method_length} lines)",
                            suggestion=f"Consider breaking this method into smaller functions",
                            confidence=confidence,
                            file_path=file_path,
                            function_name=node.name,
                            metrics={'method_length': method_length}
                        ))
        
        return smells


class ComplexConditionalRule(SmellRule):
    def __init__(self):
        super().__init__()
        self.supported_languages = ['python']
        self.max_conditions = 3
    
    def detect(self, tree: ast.AST, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                condition_count = self._count_conditions(node.test)
                if condition_count > self.max_conditions:
                    severity = Severity.HIGH if condition_count > 6 else Severity.MEDIUM
                    confidence = min(0.9, (condition_count - self.max_conditions) / self.max_conditions)
                    
                    smells.append(CodeSmell(
                        smell_type=SmellType.COMPLEX_CONDITIONAL,
                        severity=severity,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        column_start=node.col_offset,
                        column_end=node.end_col_offset or 0,
                        message=f"Complex conditional with {condition_count} conditions",
                        suggestion="Consider extracting conditions into separate variables or methods",
                        confidence=confidence,
                        file_path=file_path,
                        metrics={'condition_count': condition_count}
                    ))
        
        return smells
    
    def _count_conditions(self, node: ast.AST) -> int:
        if isinstance(node, ast.BoolOp):
            return sum(self._count_conditions(value) for value in node.values)
        elif isinstance(node, ast.Compare):
            return len(node.ops)
        else:
            return 1


class HighComplexityRule(SmellRule):
    def __init__(self):
        super().__init__()
        self.supported_languages = ['python']
        self.max_complexity = 10
    
    def detect(self, tree: ast.AST, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_complexity(node)
                if complexity > self.max_complexity:
                    severity = Severity.HIGH if complexity > 20 else Severity.MEDIUM
                    confidence = min(0.9, (complexity - self.max_complexity) / self.max_complexity)
                    
                    smells.append(CodeSmell(
                        smell_type=SmellType.HIGH_COMPLEXITY,
                        severity=severity,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        column_start=node.col_offset,
                        column_end=node.end_col_offset or 0,
                        message=f"Function '{node.name}' has high cyclomatic complexity ({complexity})",
                        suggestion="Consider refactoring to reduce complexity",
                        confidence=confidence,
                        file_path=file_path,
                        function_name=node.name,
                        metrics={'cyclomatic_complexity': complexity}
                    ))
        
        return smells
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1
        return complexity


class PoorNamingRule(SmellRule):
    def __init__(self):
        super().__init__()
        self.supported_languages = ['python']
        self.min_length = 3
    
    def detect(self, tree: ast.AST, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.name) < self.min_length or node.name.lower() in ['foo', 'bar', 'baz', 'temp', 'tmp']:
                    smells.append(CodeSmell(
                        smell_type=SmellType.POOR_NAMING,
                        severity=Severity.MEDIUM,
                        line_start=node.lineno,
                        line_end=node.lineno,
                        column_start=node.col_offset,
                        column_end=node.col_offset + len(node.name),
                        message=f"Poor function name: '{node.name}'",
                        suggestion="Use descriptive names that explain what the function does",
                        confidence=0.8,
                        file_path=file_path,
                        function_name=node.name
                    ))
        
        return smells


class LargeClassRule(SmellRule):
    def __init__(self):
        super().__init__()
        self.supported_languages = ['python']
        self.max_methods = 20
    
    def detect(self, tree: ast.AST, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                method_count = len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                if method_count > self.max_methods:
                    severity = Severity.HIGH if method_count > 30 else Severity.MEDIUM
                    confidence = min(0.9, (method_count - self.max_methods) / self.max_methods)
                    
                    smells.append(CodeSmell(
                        smell_type=SmellType.LARGE_CLASS,
                        severity=severity,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        column_start=node.col_offset,
                        column_end=node.end_col_offset or 0,
                        message=f"Class '{node.name}' has too many methods ({method_count})",
                        suggestion="Consider splitting into smaller, more focused classes",
                        confidence=confidence,
                        file_path=file_path,
                        class_name=node.name,
                        metrics={'method_count': method_count}
                    ))
        
        return smells


class DeadCodeRule(SmellRule):
    def __init__(self):
        super().__init__()
        self.supported_languages = ['python']
    
    def detect(self, tree: ast.AST, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                if isinstance(node.test, ast.Constant) and not node.test.value:
                    smells.append(CodeSmell(
                        smell_type=SmellType.DEAD_CODE,
                        severity=Severity.MEDIUM,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        column_start=node.col_offset,
                        column_end=node.end_col_offset or 0,
                        message="Dead code detected - condition is always False",
                        suggestion="Remove this unreachable code",
                        confidence=0.95,
                        file_path=file_path
                    ))
        
        return smells