# Customer Insight Platform 🎯

A full-stack web application that provides real-time customer sentiment analysis and churn prediction for any product or company.

## 🚀 Features

- **Real-time Data Scraping**: Fetch live customer reviews and comments from multiple sources
- **Sentiment Analysis**: AI-powered sentiment classification (Positive/Negative/Neutral)
- **Churn Prediction**: ML-based risk assessment for customer retention
- **Interactive Dashboard**: Beautiful visualizations of customer insights
- **Topic Modeling**: Identify key themes in customer feedback

## 🛠️ Tech Stack

### Frontend
- React.js with TypeScript
- Recharts for data visualization
- Tailwind CSS for styling
- Axios for API calls

### Backend
- FastAPI (Python)
- PostgreSQL database
- SQLAlchemy ORM
- Pydantic for data validation

### Machine Learning
- Transformers (Hugging Face) for sentiment analysis
- XGBoost for churn prediction
- scikit-learn for preprocessing
- NLTK for text processing

## 📁 Project Structure

```
project1/
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── models/        # Database models
│   │   ├── ml/            # ML models & training
│   │   ├── scrapers/      # Web scraping logic
│   │   └── core/          # Configuration
│   ├── alembic/           # Database migrations
│   └── requirements.txt
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
└── ml_training/           # ML model training notebooks
    ├── notebooks/
    └── datasets/
```

## 🎯 Current Progress

- [x] Phase 1: Database & ML Models Setup ✅
- [x] Phase 2: Backend API Development ✅
- [x] Phase 3: Frontend Development ✅
- [ ] Phase 4: Testing & Deployment

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 14+

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend

# Install Node.js first from https://nodejs.org/ if not installed
node --version  # Should be 16+

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will open at http://localhost:3000

## 👨‍💻 Author

Building this to showcase full-stack ML engineering capabilities!
