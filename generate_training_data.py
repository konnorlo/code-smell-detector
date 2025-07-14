#!/usr/bin/env python3
"""
Generate synthetic training data for better model training
"""

import os
from pathlib import Path

def generate_long_methods():
    """Generate examples of long methods."""
    examples = []
    
    for i in range(10):
        lines = ['def long_method_{}():'.format(i)]
        lines.append('    """A deliberately long method."""')
        
        # Add many lines of code
        for j in range(40 + i * 5):
            lines.append(f'    variable_{j} = {j}')
        
        lines.append(f'    return variable_{j}')
        examples.append('\n'.join(lines))
    
    return examples

def generate_complex_conditionals():
    """Generate examples of complex conditional statements."""
    examples = []
    
    for i in range(10):
        conditions = []
        for j in range(5 + i):
            conditions.append(f'x{j} > {j}')
        
        condition_str = ' and '.join(conditions)
        
        code = f"""def complex_conditional_{i}({', '.join([f'x{j}' for j in range(5 + i)])}):
    if {condition_str}:
        return True
    return False"""
        examples.append(code)
    
    return examples

def generate_poor_naming():
    """Generate examples of poor function naming."""
    poor_names = ['x', 'y', 'z', 'foo', 'bar', 'baz', 'temp', 'tmp', 'data', 'stuff', 'a', 'b', 'c']
    examples = []
    
    for i, name in enumerate(poor_names):
        code = f"""def {name}():
    return {i}"""
        examples.append(code)
    
    return examples

def generate_large_classes():
    """Generate examples of large classes."""
    examples = []
    
    for i in range(5):
        methods = []
        for j in range(25 + i * 5):
            methods.append(f'    def method_{j:02d}(self): return {j}')
        
        code = f"""class LargeClass{i}:
{chr(10).join(methods)}"""
        examples.append(code)
    
    return examples

def generate_high_complexity():
    """Generate examples of high complexity functions."""
    examples = []
    
    for i in range(10):
        nesting_levels = 3 + i // 3
        code_lines = [f'def complex_function_{i}(x):']
        
        indent = '    '
        for level in range(nesting_levels):
            code_lines.append(f'{indent}if x > {level}:')
            indent += '    '
            code_lines.append(f'{indent}for i in range({level + 1}):')
            indent += '    '
            code_lines.append(f'{indent}if i % {level + 2} == 0:')
            indent += '    '
        
        code_lines.append(f'{indent}return i')
        
        # Add return for outer levels
        for level in range(nesting_levels):
            indent = indent[:-4]
        code_lines.append('    return 0')
        
        examples.append('\n'.join(code_lines))
    
    return examples

def generate_dead_code():
    """Generate examples of dead code."""
    examples = []
    
    dead_patterns = [
        'if False:',
        'if 0:',
        'if None:',
        'if "":'
    ]
    
    for i, pattern in enumerate(dead_patterns):
        for j in range(3):
            code = f"""def function_with_dead_code_{i}_{j}():
    x = {j}
    {pattern}
        print("Dead code")
        return "never reached"
    return x"""
            examples.append(code)
    
    return examples

def generate_clean_examples():
    """Generate examples of clean, well-written code."""
    examples = []
    
    clean_functions = [
        """def calculate_area(length, width):
    \"\"\"Calculate rectangle area.\"\"\"
    return length * width""",
        
        """def find_maximum(numbers):
    \"\"\"Find maximum value in list.\"\"\"
    if not numbers:
        return None
    return max(numbers)""",
        
        """def is_valid_email(email):
    \"\"\"Check if email is valid.\"\"\"
    return '@' in email and '.' in email""",
        
        """def format_currency(amount):
    \"\"\"Format amount as currency.\"\"\"
    return f"${amount:.2f}\"""",
        
        """def fibonacci(n):
    \"\"\"Generate fibonacci number.\"\"\"
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)""",
    ]
    
    for i in range(15):
        examples.append(clean_functions[i % len(clean_functions)])
    
    return examples

def main():
    """Generate all training data files."""
    training_dir = Path('training_data/synthetic')
    training_dir.mkdir(exist_ok=True)
    
    # Generate synthetic examples
    datasets = {
        'long_methods.py': generate_long_methods(),
        'complex_conditionals.py': generate_complex_conditionals(),
        'poor_naming.py': generate_poor_naming(),
        'large_classes.py': generate_large_classes(),
        'high_complexity.py': generate_high_complexity(),
        'dead_code.py': generate_dead_code(),
        'clean_code_examples.py': generate_clean_examples(),
    }
    
    for filename, examples in datasets.items():
        file_path = training_dir / filename
        with open(file_path, 'w') as f:
            f.write('"""\nSynthetic training data\n"""\n\n')
            f.write('\n\n\n'.join(examples))
        
        print(f"Generated {len(examples)} examples in {filename}")

if __name__ == '__main__':
    main()