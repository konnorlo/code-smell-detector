import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import joblib
import json
from pathlib import Path

from ..core.models import SmellType, CodeSmell
from .feature_extractor import FeatureExtractor


class SmellPredictor:
    def __init__(self, model_type: str = 'random_forest'):
        self.model_type = model_type
        self.models = {}
        self.scalers = {}
        self.feature_extractor = FeatureExtractor()
        self.trained_smells = []
        
        self.model_classes = {
            'random_forest': RandomForestClassifier,
            'gradient_boosting': GradientBoostingClassifier,
            'logistic_regression': LogisticRegression,
            'svm': SVC
        }
    
    def train(self, training_data: List[Tuple[str, List[CodeSmell]]]) -> Dict[str, Any]:
        results = {}
        
        for smell_type in SmellType:
            if smell_type not in self.trained_smells:
                self.trained_smells.append(smell_type)
            
            X, y = self._prepare_training_data(training_data, smell_type)
            
            if len(np.unique(y)) < 2:
                print(f"Skipping {smell_type.value} - insufficient data variation")
                continue
            
            # Check if we have enough samples for training
            total_samples = len(y)
            if total_samples < 10:
                print(f"Skipping {smell_type.value} - insufficient training samples ({total_samples})")
                continue
            
            # Adjust test size for small datasets
            test_size = min(0.2, max(0.1, 2.0 / total_samples))
            
            # Check if we can use stratification
            unique_classes = np.unique(y)
            min_class_count = min(np.bincount(y))
            
            if len(unique_classes) >= 2 and min_class_count >= 2 and total_samples >= 10:
                try:
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=test_size, random_state=42, stratify=y
                    )
                except ValueError:
                    # Fallback to non-stratified split
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=test_size, random_state=42
                    )
            else:
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=test_size, random_state=42
                )
            
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            model = self._create_model()
            model.fit(X_train_scaled, y_train)
            
            y_pred = model.predict(X_test_scaled)
            
            # Adjust CV folds for small datasets
            cv_folds = min(5, len(X_train) // 2, len(np.unique(y_train)))
            if cv_folds < 2:
                cv_scores = np.array([model.score(X_train_scaled, y_train)])
            else:
                cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=cv_folds)
            
            self.models[smell_type] = model
            self.scalers[smell_type] = scaler
            
            results[smell_type.value] = {
                'accuracy': model.score(X_test_scaled, y_test),
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'classification_report': classification_report(y_test, y_pred, output_dict=True),
                'feature_importance': self._get_feature_importance(model),
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
        
        return results
    
    def predict(self, file_path: str) -> List[Dict[str, Any]]:
        features = self.feature_extractor.extract_features(file_path)
        predictions = []
        
        for smell_type in self.trained_smells:
            if smell_type in self.models:
                model = self.models[smell_type]
                scaler = self.scalers[smell_type]
                
                features_scaled = scaler.transform(features.reshape(1, -1))
                
                prediction = model.predict(features_scaled)[0]
                probability = model.predict_proba(features_scaled)[0]
                
                if prediction == 1:
                    predictions.append({
                        'smell_type': smell_type,
                        'probability': max(probability),
                        'confidence': max(probability),
                        'features': features.tolist(),
                        'feature_names': self.feature_extractor.feature_names
                    })
        
        return predictions
    
    def save_model(self, model_path: str):
        model_data = {
            'model_type': self.model_type,
            'trained_smells': [smell.value for smell in self.trained_smells],
            'feature_names': self.feature_extractor.feature_names
        }
        
        Path(model_path).mkdir(parents=True, exist_ok=True)
        
        with open(f"{model_path}/model_info.json", 'w') as f:
            json.dump(model_data, f, indent=2)
        
        for smell_type in self.trained_smells:
            if smell_type in self.models:
                joblib.dump(self.models[smell_type], f"{model_path}/{smell_type.value}_model.joblib")
                joblib.dump(self.scalers[smell_type], f"{model_path}/{smell_type.value}_scaler.joblib")
    
    def load_model(self, model_path: str):
        with open(f"{model_path}/model_info.json", 'r') as f:
            model_data = json.load(f)
        
        self.model_type = model_data['model_type']
        self.trained_smells = [SmellType(smell) for smell in model_data['trained_smells']]
        
        for smell_type in self.trained_smells:
            model_file = f"{model_path}/{smell_type.value}_model.joblib"
            scaler_file = f"{model_path}/{smell_type.value}_scaler.joblib"
            
            if Path(model_file).exists() and Path(scaler_file).exists():
                self.models[smell_type] = joblib.load(model_file)
                self.scalers[smell_type] = joblib.load(scaler_file)
    
    def _prepare_training_data(self, training_data: List[Tuple[str, List[CodeSmell]]], 
                             smell_type: SmellType) -> Tuple[np.ndarray, np.ndarray]:
        X = []
        y = []
        
        for file_path, smells in training_data:
            features = self.feature_extractor.extract_features(file_path)
            has_smell = any(smell.smell_type == smell_type for smell in smells)
            
            X.append(features)
            y.append(1 if has_smell else 0)
        
        return np.array(X), np.array(y)
    
    def _create_model(self):
        if self.model_type == 'random_forest':
            return RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
        elif self.model_type == 'gradient_boosting':
            return GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        elif self.model_type == 'logistic_regression':
            return LogisticRegression(
                random_state=42,
                max_iter=1000
            )
        elif self.model_type == 'svm':
            return SVC(
                probability=True,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def _get_feature_importance(self, model) -> Dict[str, float]:
        if hasattr(model, 'feature_importances_'):
            importances = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importances = np.abs(model.coef_[0])
        else:
            return {}
        
        return {
            name: float(importance) 
            for name, importance in zip(self.feature_extractor.feature_names, importances)
        }
    
    def get_model_info(self) -> Dict[str, Any]:
        return {
            'model_type': self.model_type,
            'trained_smells': [smell.value for smell in self.trained_smells],
            'feature_count': len(self.feature_extractor.feature_names),
            'feature_names': self.feature_extractor.feature_names
        }


class TrainingDataGenerator:
    def __init__(self):
        self.smell_detector = None
    
    def generate_training_data(self, file_paths: List[str]) -> List[Tuple[str, List[CodeSmell]]]:
        from ..detectors.smell_detector import SmellDetector
        
        if not self.smell_detector:
            self.smell_detector = SmellDetector()
        
        training_data = []
        
        for file_path in file_paths:
            try:
                analysis = self.smell_detector.detect_smells(file_path)
                training_data.append((file_path, analysis.smells))
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        return training_data
    
    def create_synthetic_smells(self, file_path: str, smell_types: List[SmellType]) -> List[CodeSmell]:
        synthetic_smells = []
        
        for smell_type in smell_types:
            smell = CodeSmell(
                smell_type=smell_type,
                severity=np.random.choice(['low', 'medium', 'high']),
                line_start=1,
                line_end=10,
                column_start=0,
                column_end=0,
                message=f"Synthetic {smell_type.value} smell",
                suggestion=f"Fix this {smell_type.value}",
                confidence=np.random.uniform(0.7, 0.9),
                file_path=file_path
            )
            synthetic_smells.append(smell)
        
        return synthetic_smells