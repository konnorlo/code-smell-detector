import unittest
import tempfile
import os
import numpy as np

from src.ml.feature_extractor import FeatureExtractor


class TestFeatureExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = FeatureExtractor()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_temp_file(self, content: str, filename: str = "test.py") -> str:
        file_path = os.path.join(self.temp_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path
    
    def test_feature_extraction_basic(self):
        simple_code = '''
def hello_world():
    print("Hello, World!")
    return True
'''
        
        file_path = self.create_temp_file(simple_code)
        features = self.extractor.extract_features(file_path)
        
        self.assertEqual(len(features), len(self.extractor.feature_names))
        self.assertIsInstance(features, np.ndarray)
        self.assertTrue(all(isinstance(f, (int, float)) for f in features))
    
    def test_lines_of_code_counting(self):
        code_with_lines = '''
# This is a comment
def function_one():
    x = 1
    y = 2
    return x + y

def function_two():
    pass
'''
        
        file_path = self.create_temp_file(code_with_lines)
        features = self.extractor.extract_features(file_path)
        
        lines_of_code_idx = self.extractor.feature_names.index('lines_of_code')
        self.assertGreater(features[lines_of_code_idx], 0)
    
    def test_complexity_metrics(self):
        complex_code = '''
def complex_function(x):
    if x > 0:
        for i in range(x):
            if i % 2 == 0:
                while i > 0:
                    if i % 3 == 0:
                        return i
                    i -= 1
    return 0
'''
        
        file_path = self.create_temp_file(complex_code)
        features = self.extractor.extract_features(file_path)
        
        complexity_idx = self.extractor.feature_names.index('cyclomatic_complexity')
        nesting_idx = self.extractor.feature_names.index('nesting_depth')
        
        self.assertGreater(features[complexity_idx], 1)
        self.assertGreater(features[nesting_idx], 1)
    
    def test_structural_metrics(self):
        structural_code = '''
import os
import sys
from pathlib import Path

class MyClass:
    def __init__(self):
        self.value = 0
    
    def method_one(self):
        return self.value
    
    def method_two(self, x, y, z):
        return x + y + z

def standalone_function():
    result = some_function_call()
    return result

lambda_func = lambda x: x * 2
'''
        
        file_path = self.create_temp_file(structural_code)
        features = self.extractor.extract_features(file_path)
        
        method_count_idx = self.extractor.feature_names.index('method_count')
        class_count_idx = self.extractor.feature_names.index('class_count')
        import_count_idx = self.extractor.feature_names.index('import_count')
        lambda_count_idx = self.extractor.feature_names.index('lambda_count')
        
        self.assertGreater(features[method_count_idx], 0)
        self.assertGreater(features[class_count_idx], 0)
        self.assertGreater(features[import_count_idx], 0)
        self.assertGreater(features[lambda_count_idx], 0)
    
    def test_lexical_metrics(self):
        lexical_code = '''
def function_with_literals():
    string_var = "Hello World"
    number_var = 42
    float_var = 3.14
    bool_var = True
    
    if number_var > 0 and bool_var:
        result = number_var + float_var
        return result
    
    return string_var
'''
        
        file_path = self.create_temp_file(lexical_code)
        features = self.extractor.extract_features(file_path)
        
        string_idx = self.extractor.feature_names.index('string_literal_count')
        numeric_idx = self.extractor.feature_names.index('numeric_literal_count')
        boolean_idx = self.extractor.feature_names.index('boolean_literal_count')
        comparison_idx = self.extractor.feature_names.index('comparison_count')
        
        self.assertGreater(features[string_idx], 0)
        self.assertGreater(features[numeric_idx], 0)
        self.assertGreaterEqual(features[boolean_idx], 0)
        self.assertGreater(features[comparison_idx], 0)
    
    def test_style_metrics(self):
        poorly_styled_code = '''def function():
    x = 1
    y = 2
    return x + y

def another_function():
    return True
    return True'''
        
        file_path = self.create_temp_file(poorly_styled_code)
        features = self.extractor.extract_features(file_path)
        
        indentation_idx = self.extractor.feature_names.index('indentation_inconsistency')
        duplicate_idx = self.extractor.feature_names.index('duplicate_line_ratio')
        
        self.assertGreaterEqual(features[indentation_idx], 0)
        self.assertGreaterEqual(features[duplicate_idx], 0)
    
    def test_empty_file(self):
        empty_code = ""
        
        file_path = self.create_temp_file(empty_code)
        features = self.extractor.extract_features(file_path)
        
        self.assertEqual(len(features), len(self.extractor.feature_names))
        self.assertTrue(all(f >= 0 for f in features))
    
    def test_feature_names_consistency(self):
        simple_code = '''
def test():
    pass
'''
        
        file_path = self.create_temp_file(simple_code)
        features = self.extractor.extract_features(file_path)
        
        self.assertEqual(len(features), len(self.extractor.feature_names))
        
        # Check that all feature names are strings
        self.assertTrue(all(isinstance(name, str) for name in self.extractor.feature_names))
        
        # Check that feature names are unique
        self.assertEqual(len(self.extractor.feature_names), len(set(self.extractor.feature_names)))
    
    def test_non_python_file(self):
        non_python_file = self.create_temp_file("Not Python code", "test.txt")
        features = self.extractor.extract_features(non_python_file)
        
        # Should return zeros for non-Python files
        self.assertTrue(all(f == 0 for f in features))


if __name__ == '__main__':
    unittest.main()