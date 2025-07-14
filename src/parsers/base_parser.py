from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import ast
from pathlib import Path

from ..core.models import CodeMetrics, FileAnalysis


class BaseParser(ABC):
    def __init__(self):
        self.supported_extensions = []
    
    @abstractmethod
    def parse_file(self, file_path: str) -> FileAnalysis:
        pass
    
    @abstractmethod
    def extract_metrics(self, tree: Any) -> CodeMetrics:
        pass
    
    @abstractmethod
    def get_functions(self, tree: Any) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def get_classes(self, tree: Any) -> List[Dict[str, Any]]:
        pass
    
    def can_parse(self, file_path: str) -> bool:
        return Path(file_path).suffix in self.supported_extensions
    
    def read_file(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def count_lines(self, content: str) -> int:
        return len([line for line in content.split('\n') if line.strip()])


class PythonParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.py']
    
    def parse_file(self, file_path: str) -> FileAnalysis:
        content = self.read_file(file_path)
        tree = ast.parse(content)
        
        metrics = self.extract_metrics(tree)
        lines_of_code = self.count_lines(content)
        
        return FileAnalysis(
            file_path=file_path,
            language='python',
            lines_of_code=lines_of_code,
            smells=[],
            metrics=metrics.to_dict()
        )
    
    def extract_metrics(self, tree: ast.AST) -> CodeMetrics:
        visitor = MetricsVisitor()
        visitor.visit(tree)
        
        return CodeMetrics(
            cyclomatic_complexity=visitor.cyclomatic_complexity,
            lines_of_code=visitor.lines_of_code,
            cognitive_complexity=visitor.cognitive_complexity,
            nesting_depth=visitor.max_nesting_depth,
            parameter_count=visitor.max_parameters,
            variable_count=visitor.variable_count,
            duplicate_lines=0,
            maintainability_index=0.0,
            halstead_difficulty=0.0
        )
    
    def get_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'line_start': node.lineno,
                    'line_end': node.end_lineno,
                    'args': len(node.args.args),
                    'decorators': len(node.decorator_list),
                    'is_async': isinstance(node, ast.AsyncFunctionDef)
                })
        return functions
    
    def get_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                classes.append({
                    'name': node.name,
                    'line_start': node.lineno,
                    'line_end': node.end_lineno,
                    'methods': len(methods),
                    'decorators': len(node.decorator_list),
                    'bases': len(node.bases)
                })
        return classes


class MetricsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.cyclomatic_complexity = 1
        self.lines_of_code = 0
        self.cognitive_complexity = 0
        self.nesting_depth = 0
        self.max_nesting_depth = 0
        self.max_parameters = 0
        self.variable_count = 0
        self.current_nesting = 0
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.max_parameters = max(self.max_parameters, len(node.args.args))
        self.generic_visit(node)
    
    def visit_If(self, node: ast.If):
        self.cyclomatic_complexity += 1
        self.cognitive_complexity += 1
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_For(self, node: ast.For):
        self.cyclomatic_complexity += 1
        self.cognitive_complexity += 1
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_While(self, node: ast.While):
        self.cyclomatic_complexity += 1
        self.cognitive_complexity += 1
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
        self.generic_visit(node)
        self.current_nesting -= 1
    
    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        self.cyclomatic_complexity += 1
        self.cognitive_complexity += 1
        self.generic_visit(node)
    
    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Store):
            self.variable_count += 1
        self.generic_visit(node)