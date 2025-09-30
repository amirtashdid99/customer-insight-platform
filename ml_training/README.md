# ML Training Module

This directory contains Jupyter notebooks and scripts for training the machine learning models.

## Models to Train

### 1. Churn Prediction Model (XGBoost)
- **Dataset**: Telco Customer Churn Dataset
- **Algorithm**: XGBoost Classifier
- **Features**: Customer demographics, usage patterns, contract info
- **Output**: Churn probability (0-1)

### 2. Sentiment Analysis Model
- **Option A**: Fine-tune DistilBERT on domain-specific data
- **Option B**: Use pre-trained model from Hugging Face
- **Output**: Sentiment (positive/negative/neutral) + confidence score

## Directory Structure

```
ml_training/
├── notebooks/
│   ├── 01_churn_model_training.ipynb
│   └── 02_sentiment_model_selection.ipynb
├── datasets/
│   ├── .gitkeep
│   └── README.md  (instructions to download datasets)
└── scripts/
    ├── train_churn_model.py
    └── evaluate_models.py
```

## Getting Started

1. Download the Telco Customer Churn dataset from Kaggle
2. Place it in `datasets/` directory
3. Run the Jupyter notebooks in order
4. Trained models will be saved to `../trained_models/`
