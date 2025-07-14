# Code Smell Detector

An AI-powered tool that analyzes code to identify potential code smells and predict sections likely to cause future bugs.

## Features

- **AST-based Analysis**: Parses code into Abstract Syntax Trees for deep structural analysis
- **Machine Learning Detection**: Uses trained models to identify code smell patterns
- **Multi-language Support**: Supports Python, JavaScript, and more
- **CLI Interface**: Easy-to-use command-line tool
- **Detailed Reports**: Provides explanations and suggestions for detected issues

## Architecture

1. **Code Parser**: Converts source code to AST representations
2. **Feature Extractor**: Extracts relevant metrics and patterns
3. **ML Model**: Trained classifier for smell detection
4. **Reporter**: Generates human-readable reports with suggestions

## Supported Code Smells

- Long methods/functions
- Complex conditional logic
- Duplicate code patterns
- Poor naming conventions
- High cyclomatic complexity
- Tight coupling indicators
- Dead code detection


  # Analyze files for code smells
  python cli.py analyze example_code.py

  # Use ML predictions
  python cli.py analyze example_code.py --ml-predict

  # Train new model
  python cli.py train training_data --model-type random_forest

  # Get detailed explanations
  python cli.py explain example_code.py