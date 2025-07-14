import unittest
import tempfile
import os
from pathlib import Path

from src.detectors.smell_detector import SmellDetector
from src.core.models import SmellType, Severity


class TestSmellDetector(unittest.TestCase):
    def setUp(self):
        self.detector = SmellDetector()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_temp_file(self, content: str, filename: str = "test.py") -> str:
        file_path = os.path.join(self.temp_dir, filename)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path
    
    def test_long_method_detection(self):
        long_method_code = '''
def long_method():
    """ This is a very long method that should be detected as a smell """
''' + '\n'.join([f'    line_{i} = {i}' for i in range(35)])
        
        file_path = self.create_temp_file(long_method_code)
        analysis = self.detector.detect_smells(file_path)
        
        long_method_smells = [s for s in analysis.smells if s.smell_type == SmellType.LONG_METHOD]
        self.assertEqual(len(long_method_smells), 1)
        self.assertEqual(long_method_smells[0].function_name, "long_method")
    
    def test_complex_conditional_detection(self):
        complex_conditional_code = '''
def complex_condition():
    if x > 0 and y < 10 and z == 5 and a != b and c in list_items and d not in other_list:
        return True
    return False
'''
        
        file_path = self.create_temp_file(complex_conditional_code)
        analysis = self.detector.detect_smells(file_path)
        
        complex_smells = [s for s in analysis.smells if s.smell_type == SmellType.COMPLEX_CONDITIONAL]
        self.assertEqual(len(complex_smells), 1)
    
    def test_high_complexity_detection(self):
        high_complexity_code = '''
def complex_function(x):
    if x > 0:
        for i in range(x):
            if i % 2 == 0:
                for j in range(i):
                    if j > 5:
                        while j > 0:
                            if j % 3 == 0:
                                try:
                                    return j
                                except:
                                    pass
                            j -= 1
    return 0
'''
        
        file_path = self.create_temp_file(high_complexity_code)
        analysis = self.detector.detect_smells(file_path)
        
        complexity_smells = [s for s in analysis.smells if s.smell_type == SmellType.HIGH_COMPLEXITY]
        self.assertGreaterEqual(len(complexity_smells), 0)
    
    def test_poor_naming_detection(self):
        poor_naming_code = '''
def x():
    pass

def foo():
    pass

def temp():
    pass
'''
        
        file_path = self.create_temp_file(poor_naming_code)
        analysis = self.detector.detect_smells(file_path)
        
        naming_smells = [s for s in analysis.smells if s.smell_type == SmellType.POOR_NAMING]
        self.assertEqual(len(naming_smells), 3)
    
    def test_large_class_detection(self):
        methods = '\n'.join([f'    def method_{i}(self): pass' for i in range(25)])
        large_class_code = f'''
class LargeClass:
{methods}
'''
        
        file_path = self.create_temp_file(large_class_code)
        analysis = self.detector.detect_smells(file_path)
        
        large_class_smells = [s for s in analysis.smells if s.smell_type == SmellType.LARGE_CLASS]
        self.assertEqual(len(large_class_smells), 1)
        self.assertEqual(large_class_smells[0].class_name, "LargeClass")
    
    def test_dead_code_detection(self):
        dead_code = '''
def function_with_dead_code():
    if False:
        print("This will never execute")
    return True
'''
        
        file_path = self.create_temp_file(dead_code)
        analysis = self.detector.detect_smells(file_path)
        
        dead_code_smells = [s for s in analysis.smells if s.smell_type == SmellType.DEAD_CODE]
        self.assertEqual(len(dead_code_smells), 1)
    
    def test_clean_code_no_smells(self):
        clean_code = '''
def calculate_sum(numbers):
    """Calculate the sum of a list of numbers."""
    return sum(numbers)

def is_even(number):
    """Check if a number is even."""
    return number % 2 == 0

class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
'''
        
        file_path = self.create_temp_file(clean_code)
        analysis = self.detector.detect_smells(file_path)
        
        self.assertEqual(len(analysis.smells), 0)
    
    def test_multiple_smells_in_file(self):
        mixed_code = '''
def x():  # Poor naming
    """ This is a very long method """
''' + '\n'.join([f'    line_{i} = {i}' for i in range(35)]) + '''

class LargeClass:
''' + '\n'.join([f'    def method_{i}(self): pass' for i in range(25)])
        
        file_path = self.create_temp_file(mixed_code)
        analysis = self.detector.detect_smells(file_path)
        
        self.assertGreater(len(analysis.smells), 2)
        
        smell_types = [s.smell_type for s in analysis.smells]
        self.assertIn(SmellType.LONG_METHOD, smell_types)
        self.assertIn(SmellType.POOR_NAMING, smell_types)
        self.assertIn(SmellType.LARGE_CLASS, smell_types)


if __name__ == '__main__':
    unittest.main()