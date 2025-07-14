import ast
import numpy as np
from typing import List, Dict, Any, Tuple
from collections import Counter

from ..core.models import CodeMetrics, FileAnalysis
from ..parsers.base_parser import PythonParser


class FeatureExtractor:
    def __init__(self):
        self.feature_names = [
            'lines_of_code',
            'cyclomatic_complexity',
            'nesting_depth',
            'parameter_count',
            'variable_count',
            'method_count',
            'class_count',
            'import_count',
            'comment_ratio',
            'string_literal_count',
            'numeric_literal_count',
            'boolean_literal_count',
            'function_call_count',
            'loop_count',
            'conditional_count',
            'exception_handler_count',
            'decorator_count',
            'lambda_count',
            'comprehension_count',
            'yield_count',
            'return_count',
            'assignment_count',
            'comparison_count',
            'arithmetic_op_count',
            'logical_op_count',
            'avg_line_length',
            'max_line_length',
            'empty_line_ratio',
            'indentation_inconsistency',
            'duplicate_line_ratio'
        ]
    
    def extract_features(self, file_path: str) -> np.ndarray:
        parser = PythonParser()
        
        if not parser.can_parse(file_path):
            return np.zeros(len(self.feature_names))
        
        content = parser.read_file(file_path)
        tree = ast.parse(content)
        
        features = {}
        
        features.update(self._extract_basic_metrics(tree, content))
        features.update(self._extract_structural_metrics(tree))
        features.update(self._extract_lexical_metrics(tree))
        features.update(self._extract_style_metrics(content))
        
        return np.array([features.get(name, 0) for name in self.feature_names])
    
    def _extract_basic_metrics(self, tree: ast.AST, content: str) -> Dict[str, float]:
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        return {
            'lines_of_code': len(non_empty_lines),
            'comment_ratio': self._calculate_comment_ratio(lines),
            'avg_line_length': np.mean([len(line) for line in non_empty_lines]) if non_empty_lines else 0,
            'max_line_length': max([len(line) for line in lines]) if lines else 0,
            'empty_line_ratio': (len(lines) - len(non_empty_lines)) / len(lines) if lines else 0
        }
    
    def _extract_structural_metrics(self, tree: ast.AST) -> Dict[str, float]:
        visitor = StructuralMetricsVisitor()
        visitor.visit(tree)
        
        return {
            'cyclomatic_complexity': visitor.cyclomatic_complexity,
            'nesting_depth': visitor.max_nesting_depth,
            'parameter_count': visitor.total_parameters,
            'variable_count': visitor.variable_count,
            'method_count': visitor.method_count,
            'class_count': visitor.class_count,
            'import_count': visitor.import_count,
            'function_call_count': visitor.function_call_count,
            'loop_count': visitor.loop_count,
            'conditional_count': visitor.conditional_count,
            'exception_handler_count': visitor.exception_handler_count,
            'decorator_count': visitor.decorator_count,
            'lambda_count': visitor.lambda_count,
            'comprehension_count': visitor.comprehension_count,
            'yield_count': visitor.yield_count,
            'return_count': visitor.return_count,
            'assignment_count': visitor.assignment_count
        }
    
    def _extract_lexical_metrics(self, tree: ast.AST) -> Dict[str, float]:
        visitor = LexicalMetricsVisitor()
        visitor.visit(tree)
        
        return {
            'string_literal_count': visitor.string_literal_count,
            'numeric_literal_count': visitor.numeric_literal_count,
            'boolean_literal_count': visitor.boolean_literal_count,
            'comparison_count': visitor.comparison_count,
            'arithmetic_op_count': visitor.arithmetic_op_count,
            'logical_op_count': visitor.logical_op_count
        }
    
    def _extract_style_metrics(self, content: str) -> Dict[str, float]:
        lines = content.split('\n')
        
        indentation_levels = []
        for line in lines:
            if line.strip():
                indentation = len(line) - len(line.lstrip())
                indentation_levels.append(indentation)
        
        indentation_inconsistency = 0
        if indentation_levels:
            common_indent = Counter(indentation_levels).most_common(1)[0][0]
            indentation_inconsistency = sum(1 for level in indentation_levels if level != common_indent and level != 0) / len(indentation_levels)
        
        duplicate_lines = self._find_duplicate_lines(lines)
        duplicate_ratio = len(duplicate_lines) / len(lines) if lines else 0
        
        return {
            'indentation_inconsistency': indentation_inconsistency,
            'duplicate_line_ratio': duplicate_ratio
        }
    
    def _calculate_comment_ratio(self, lines: List[str]) -> float:
        comment_lines = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
                comment_lines += 1
        
        return comment_lines / len(lines) if lines else 0
    
    def _find_duplicate_lines(self, lines: List[str]) -> List[str]:
        line_counts = Counter(line.strip() for line in lines if line.strip())
        return [line for line, count in line_counts.items() if count > 1]


class StructuralMetricsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.cyclomatic_complexity = 1
        self.max_nesting_depth = 0
        self.current_nesting = 0
        self.total_parameters = 0
        self.variable_count = 0
        self.method_count = 0
        self.class_count = 0
        self.import_count = 0
        self.function_call_count = 0
        self.loop_count = 0
        self.conditional_count = 0
        self.exception_handler_count = 0
        self.decorator_count = 0
        self.lambda_count = 0
        self.comprehension_count = 0
        self.yield_count = 0
        self.return_count = 0
        self.assignment_count = 0
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.method_count += 1
        self.total_parameters += len(node.args.args)
        self.decorator_count += len(node.decorator_list)
        self.generic_visit(node)
    
    def visit_ClassDef(self, node: ast.ClassDef):
        self.class_count += 1
        self.decorator_count += len(node.decorator_list)
        self.generic_visit(node)
    
    def visit_Import(self, node: ast.Import):
        self.import_count += len(node.names)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom):
        self.import_count += len(node.names)
        self.generic_visit(node)
    
    def visit_Call(self, node: ast.Call):
        self.function_call_count += 1
        self.generic_visit(node)
    
    def visit_If(self, node: ast.If):
        self.cyclomatic_complexity += 1
        self.conditional_count += 1
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_For(self, node: ast.For):
        self.cyclomatic_complexity += 1
        self.loop_count += 1
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_While(self, node: ast.While):
        self.cyclomatic_complexity += 1
        self.loop_count += 1
        self._enter_block()
        self.generic_visit(node)
        self._exit_block()
    
    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        self.cyclomatic_complexity += 1
        self.exception_handler_count += 1
        self.generic_visit(node)
    
    def visit_Lambda(self, node: ast.Lambda):
        self.lambda_count += 1
        self.generic_visit(node)
    
    def visit_ListComp(self, node: ast.ListComp):
        self.comprehension_count += 1
        self.generic_visit(node)
    
    def visit_SetComp(self, node: ast.SetComp):
        self.comprehension_count += 1
        self.generic_visit(node)
    
    def visit_DictComp(self, node: ast.DictComp):
        self.comprehension_count += 1
        self.generic_visit(node)
    
    def visit_GeneratorExp(self, node: ast.GeneratorExp):
        self.comprehension_count += 1
        self.generic_visit(node)
    
    def visit_Yield(self, node: ast.Yield):
        self.yield_count += 1
        self.generic_visit(node)
    
    def visit_YieldFrom(self, node: ast.YieldFrom):
        self.yield_count += 1
        self.generic_visit(node)
    
    def visit_Return(self, node: ast.Return):
        self.return_count += 1
        self.generic_visit(node)
    
    def visit_Assign(self, node: ast.Assign):
        self.assignment_count += 1
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variable_count += 1
        self.generic_visit(node)
    
    def _enter_block(self):
        self.current_nesting += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_nesting)
    
    def _exit_block(self):
        self.current_nesting -= 1


class LexicalMetricsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.string_literal_count = 0
        self.numeric_literal_count = 0
        self.boolean_literal_count = 0
        self.comparison_count = 0
        self.arithmetic_op_count = 0
        self.logical_op_count = 0
    
    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, str):
            self.string_literal_count += 1
        elif isinstance(node.value, (int, float)):
            self.numeric_literal_count += 1
        elif isinstance(node.value, bool):
            self.boolean_literal_count += 1
        self.generic_visit(node)
    
    def visit_Compare(self, node: ast.Compare):
        self.comparison_count += len(node.ops)
        self.generic_visit(node)
    
    def visit_BinOp(self, node: ast.BinOp):
        if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow)):
            self.arithmetic_op_count += 1
        self.generic_visit(node)
    
    def visit_BoolOp(self, node: ast.BoolOp):
        self.logical_op_count += 1
        self.generic_visit(node)