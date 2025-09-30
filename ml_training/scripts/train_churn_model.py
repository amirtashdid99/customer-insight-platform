"""
Churn Prediction Model Training Script

This script trains an XGBoost classifier on the Telco Customer Churn dataset
and saves the model for use in the API.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import xgboost as xgb
import joblib
from pathlib import Path
import json


class ChurnModelTrainer:
    """Trainer class for churn prediction model"""
    
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None
        
    def load_and_preprocess_data(self):
        """Load and preprocess the Telco dataset"""
        print("Loading data...")
        df = pd.read_csv(self.data_path)
        
        # Handle missing values
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
        
        # Drop customerID (not useful for prediction)
        df = df.drop('customerID', axis=1)
        
        # Encode target variable
        df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
        
        # Separate features and target
        X = df.drop('Churn', axis=1)
        y = df['Churn']
        
        # Identify categorical columns
        categorical_cols = X.select_dtypes(include=['object']).columns
        
        # Encode categorical variables
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            self.label_encoders[col] = le
        
        self.feature_names = X.columns.tolist()
        
        return X, y
    
    def train_model(self, X, y):
        """Train XGBoost model with optimized hyperparameters"""
        print("\nSplitting data...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        print("Scaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train XGBoost model
        print("\nTraining XGBoost model...")
        self.model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            gamma=1,
            reg_alpha=0.1,
            reg_lambda=1,
            random_state=42,
            eval_metric='logloss'
        )
        
        self.model.fit(
            X_train_scaled, y_train,
            eval_set=[(X_test_scaled, y_test)],
            verbose=True
        )
        
        # Evaluate model
        print("\nEvaluating model...")
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        print(f"\nROC-AUC Score: {roc_auc_score(y_test, y_pred_proba):.4f}")
        
        # Cross-validation
        cv_scores = cross_val_score(
            self.model, X_train_scaled, y_train, cv=5, scoring='roc_auc'
        )
        print(f"Cross-validation ROC-AUC: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        return X_test_scaled, y_test
    
    def save_model(self, output_dir: str):
        """Save the trained model and preprocessing objects"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\nSaving model to {output_dir}...")
        
        # Save model
        model_path = output_path / "churn_model.pkl"
        joblib.dump(self.model, model_path)
        
        # Save scaler
        scaler_path = output_path / "scaler.pkl"
        joblib.dump(self.scaler, scaler_path)
        
        # Save label encoders
        encoders_path = output_path / "label_encoders.pkl"
        joblib.dump(self.label_encoders, encoders_path)
        
        # Save feature names
        features_path = output_path / "feature_names.json"
        with open(features_path, 'w') as f:
            json.dump(self.feature_names, f)
        
        # Save feature importance
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        importance_path = output_path / "feature_importance.csv"
        importance_df.to_csv(importance_path, index=False)
        
        print("Model saved successfully!")
        print(f"\nTop 10 Important Features:")
        print(importance_df.head(10))


def main():
    """Main training pipeline"""
    # Paths
    data_path = "../ml_training/datasets/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    output_dir = "../trained_models"
    
    # Initialize trainer
    trainer = ChurnModelTrainer(data_path)
    
    # Load and preprocess data
    X, y = trainer.load_and_preprocess_data()
    
    # Train model
    X_test, y_test = trainer.train_model(X, y)
    
    # Save model
    trainer.save_model(output_dir)
    
    print("\n" + "="*50)
    print("Training completed successfully!")
    print("="*50)


if __name__ == "__main__":
    main()
