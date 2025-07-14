#!/usr/bin/env python3

import click
import json
from pathlib import Path
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel
from rich.syntax import Syntax

from src.detectors.smell_detector import SmellDetector
from src.ml.model import SmellPredictor, TrainingDataGenerator
from src.core.models import SmellType, Severity


console = Console()


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Code Smell Detector - AI-powered code analysis tool"""
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file for results')
@click.option('--format', '-f', type=click.Choice(['json', 'table', 'detailed']), default='table', help='Output format')
@click.option('--severity', '-s', type=click.Choice(['low', 'medium', 'high', 'critical']), help='Filter by severity')
@click.option('--smell-type', '-t', help='Filter by smell type')
@click.option('--ml-predict', is_flag=True, help='Use ML model for prediction')
def analyze(path: str, output: str, format: str, severity: str, smell_type: str, ml_predict: bool):
    """Analyze code for smells in a file or directory"""
    
    detector = SmellDetector()
    predictor = None
    
    if ml_predict:
        predictor = SmellPredictor()
        model_path = Path('models')
        if model_path.exists():
            try:
                predictor.load_model(str(model_path))
                console.print("[green]Loaded ML model successfully[/green]")
            except Exception as e:
                console.print(f"[yellow]Warning: Could not load ML model: {e}[/yellow]")
                predictor = None
    
    path_obj = Path(path)
    files_to_analyze = []
    
    if path_obj.is_file():
        files_to_analyze = [str(path_obj)]
    else:
        files_to_analyze = [str(f) for f in path_obj.rglob('*.py')]
    
    all_results = []
    
    with Progress() as progress:
        task = progress.add_task("[green]Analyzing files...", total=len(files_to_analyze))
        
        for file_path in files_to_analyze:
            try:
                analysis = detector.detect_smells(file_path)
                
                if predictor:
                    ml_predictions = predictor.predict(file_path)
                    for pred in ml_predictions:
                        # Convert ML prediction to CodeSmell for consistency
                        pass
                
                filtered_smells = analysis.smells
                
                if severity:
                    filtered_smells = [s for s in filtered_smells if s.severity.value == severity]
                
                if smell_type:
                    filtered_smells = [s for s in filtered_smells if s.smell_type.value == smell_type]
                
                if filtered_smells:
                    all_results.append({
                        'file': file_path,
                        'smells': filtered_smells,
                        'metrics': analysis.metrics
                    })
                
                progress.update(task, advance=1)
                
            except Exception as e:
                console.print(f"[red]Error analyzing {file_path}: {e}[/red]")
                progress.update(task, advance=1)
    
    if format == 'json':
        _output_json(all_results, output)
    elif format == 'table':
        _output_table(all_results)
    elif format == 'detailed':
        _output_detailed(all_results)


@cli.command()
@click.argument('training_dir', type=click.Path(exists=True))
@click.option('--model-type', '-m', type=click.Choice(['random_forest', 'gradient_boosting', 'logistic_regression', 'svm']), default='random_forest')
@click.option('--output-dir', '-o', type=click.Path(), default='models')
def train(training_dir: str, model_type: str, output_dir: str):
    """Train ML model on code samples"""
    
    console.print(f"[blue]Training {model_type} model...[/blue]")
    
    training_files = list(Path(training_dir).rglob('*.py'))
    
    if not training_files:
        console.print("[red]No Python files found in training directory[/red]")
        return
    
    generator = TrainingDataGenerator()
    training_data = generator.generate_training_data([str(f) for f in training_files])
    
    if not training_data:
        console.print("[red]No training data generated[/red]")
        return
    
    predictor = SmellPredictor(model_type=model_type)
    
    with Progress() as progress:
        task = progress.add_task("[green]Training model...", total=100)
        
        results = predictor.train(training_data)
        progress.update(task, advance=100)
    
    predictor.save_model(output_dir)
    
    console.print(f"[green]Model trained and saved to {output_dir}[/green]")
    
    # Display training results
    table = Table(title="Training Results")
    table.add_column("Smell Type")
    table.add_column("Accuracy")
    table.add_column("CV Score")
    table.add_column("Samples")
    
    for smell_type, metrics in results.items():
        table.add_row(
            smell_type,
            f"{metrics['accuracy']:.3f}",
            f"{metrics['cv_mean']:.3f} ± {metrics['cv_std']:.3f}",
            str(metrics['training_samples'])
        )
    
    console.print(table)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--model-dir', '-m', type=click.Path(), default='models')
def predict(file_path: str, model_dir: str):
    """Predict code smells using trained ML model"""
    
    model_path = Path(model_dir)
    if not model_path.exists():
        console.print(f"[red]Model directory {model_dir} not found[/red]")
        return
    
    predictor = SmellPredictor()
    
    try:
        predictor.load_model(str(model_path))
        console.print("[green]Model loaded successfully[/green]")
    except Exception as e:
        console.print(f"[red]Error loading model: {e}[/red]")
        return
    
    predictions = predictor.predict(file_path)
    
    if not predictions:
        console.print("[green]No code smells predicted[/green]")
        return
    
    console.print(f"[blue]Predictions for {file_path}:[/blue]")
    
    for pred in predictions:
        panel = Panel(
            f"Smell Type: {pred['smell_type'].value}\n"
            f"Confidence: {pred['confidence']:.3f}\n"
            f"Probability: {pred['probability']:.3f}",
            title=f"Predicted Smell",
            border_style="yellow"
        )
        console.print(panel)


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def explain(file_path: str):
    """Explain detected code smells with suggestions"""
    
    detector = SmellDetector()
    analysis = detector.detect_smells(file_path)
    
    if not analysis.smells:
        console.print("[green]No code smells detected[/green]")
        return
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    for smell in analysis.smells:
        console.print(f"\n[red]Found: {smell.smell_type.value}[/red]")
        
        panel = Panel(
            f"Severity: {smell.severity.value}\n"
            f"Location: Lines {smell.line_start}-{smell.line_end}\n"
            f"Message: {smell.message}\n"
            f"Suggestion: {smell.suggestion}\n"
            f"Confidence: {smell.confidence:.2f}",
            title=f"{smell.smell_type.value.title()} Smell",
            border_style="red"
        )
        console.print(panel)
        
        # Show code snippet
        lines = content.split('\n')
        start_line = max(0, smell.line_start - 3)
        end_line = min(len(lines), smell.line_end + 3)
        
        code_snippet = '\n'.join(lines[start_line:end_line])
        syntax = Syntax(code_snippet, "python", line_numbers=True, start_line=start_line + 1)
        console.print(syntax)


def _output_json(results: List[Dict], output_file: str = None):
    """Output results in JSON format"""
    json_results = []
    
    for result in results:
        json_smells = []
        for smell in result['smells']:
            json_smells.append({
                'type': smell.smell_type.value,
                'severity': smell.severity.value,
                'line_start': smell.line_start,
                'line_end': smell.line_end,
                'message': smell.message,
                'suggestion': smell.suggestion,
                'confidence': smell.confidence
            })
        
        json_results.append({
            'file': result['file'],
            'smells': json_smells,
            'metrics': result['metrics']
        })
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(json_results, f, indent=2)
        console.print(f"[green]Results saved to {output_file}[/green]")
    else:
        console.print(json.dumps(json_results, indent=2))


def _output_table(results: List[Dict]):
    """Output results in table format"""
    table = Table(title="Code Smell Analysis Results")
    table.add_column("File")
    table.add_column("Smell Type")
    table.add_column("Severity")
    table.add_column("Line")
    table.add_column("Message")
    
    for result in results:
        file_path = result['file']
        for smell in result['smells']:
            table.add_row(
                file_path,
                smell.smell_type.value,
                smell.severity.value,
                f"{smell.line_start}-{smell.line_end}",
                smell.message[:50] + "..." if len(smell.message) > 50 else smell.message
            )
    
    console.print(table)


def _output_detailed(results: List[Dict]):
    """Output detailed results"""
    for result in results:
        console.print(f"\n[blue]File: {result['file']}[/blue]")
        
        if not result['smells']:
            console.print("[green]No smells detected[/green]")
            continue
        
        for smell in result['smells']:
            severity_color = {
                'low': 'yellow',
                'medium': 'orange',
                'high': 'red',
                'critical': 'bright_red'
            }.get(smell.severity.value, 'white')
            
            console.print(f"  [{severity_color}]{smell.smell_type.value}[/{severity_color}] "
                         f"(Line {smell.line_start}-{smell.line_end})")
            console.print(f"    {smell.message}")
            console.print(f"    Suggestion: {smell.suggestion}")
            console.print(f"    Confidence: {smell.confidence:.2f}")
            console.print()


if __name__ == '__main__':
    cli()