# Customer Insight Platform 🎯

**A full-stack AI-powered customer sentiment analysis and churn prediction platform with enterprise features.**

Analyzes customer reviews from multiple sources to provide actionable business intelligence with real-time alerts and user accounts.

## Developer

**Amir Hossein Nasserpour**
- Email: amirtashdid99@gmail.com
- Telegram: [@R00T99](https://t.me/R00T99)
- GitHub: [@amirtashdid99](https://github.com/amirtashdid99)

## 🚀 Features

### Core AI/ML Features
- **Real-time Data Scraping**: Fetch live customer reviews from multiple sources (Reddit, Twitter, Review Sites)
- **Sentiment Analysis**: AI-powered classification using DistilBERT transformer (95%+ accuracy)
- **Churn Prediction**: ML-based customer retention risk assessment using XGBoost
- **Topic Modeling**: Automatic identification of key themes in customer feedback
- **Interactive Dashboard**: Beautiful real-time visualizations with Recharts

### 🎉 Enterprise Features
- **🔐 User Authentication**: Secure JWT-based login system with bcrypt password hashing
- **📧 Smart Email Alerts**: Automatic notifications when sentiment spikes are detected (>20% change)
- **⭐ Saved Products**: Personal dashboard to track favorite products over time
- **📊 Sentiment Tracking**: Monitor sentiment trends and get proactive alerts
- **🎨 Responsive Design**: Mobile-first UI that works on all devices

## 🛠️ Tech Stack

### Frontend
- React.js with TypeScript
- Recharts for data visualization
- Responsive CSS with media queries
- Axios for API calls

### Backend
- FastAPI (Python) with automatic OpenAPI docs
- PostgreSQL/SQLite database
- SQLAlchemy ORM
- Pydantic for data validation
- **JWT Authentication** with python-jose
- **Bcrypt Password Hashing** with passlib
- Email integration with SMTP

### Machine Learning
- Transformers (Hugging Face) for sentiment analysis (DistilBERT)
- XGBoost for churn prediction
- scikit-learn for preprocessing
- NLTK for text processing

### Infrastructure
- **Celery** - Distributed task queue for background processing
- **Redis** - Message broker and caching
- **BeautifulSoup & aiohttp** - Web scraping
- **Render** - Backend hosting (512MB free tier)
- **Vercel** - Frontend hosting

## 📁 Project Structure

```
customer-insight-platform/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/             # API endpoints (analysis, auth, notifications)
│   │   ├── core/            # Configuration & database
│   │   ├── ml/              # ML models (sentiment, churn)
│   │   ├── models/          # Database & Pydantic models
│   │   ├── scrapers/        # Web scraping logic
│   │   └── tasks/           # Background tasks
│   ├── alembic/             # Database migrations
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API client
│   │   └── App.tsx          # Main application
│   └── package.json         # Node dependencies
├── ml_training/             # ML model training scripts
│   ├── notebooks/           # Jupyter notebooks
│   └── datasets/            # Training data
└── trained_models/          # Saved ML models
```

## 🎯 Project Status

- ✅ Database & ML Models Setup
- ✅ Backend API Development (FastAPI + Authentication)
- ✅ Frontend Development (React + TypeScript)
- ✅ Deployment (Render + Vercel)
- ✅ Enterprise Features (Auth, Alerts, Saved Products)

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- Redis server (for full mode with background tasks)
- PostgreSQL 14+ (optional, SQLite works for development)

### 1. Clone Repository

```bash

git clone https://github.com/amirtashdid99/customer-insight-platform.git### Backend Setup

cd customer-insight-platform```bash

```cd backend

python -m venv venv

### 2. Backend Setupvenv\Scripts\activate  # Windows

pip install -r requirements.txt

#### Install Redis```

**Windows (Chocolatey):**

```powershell### Frontend Setup

choco install redis-64```bash

redis-servercd frontend

```

# Install Node.js first from https://nodejs.org/ if not installed

**macOS:**node --version  # Should be 16+

```bash

brew install redis# Install dependencies

brew services start redisnpm install

```

# Start development server

**Linux:**npm start

```bash```

sudo apt-get install redis-server

sudo systemctl start redisThe frontend will open at http://localhost:3000

```

## 👨‍💻 Author

#### Setup Python Environment

```bashBuilding this to showcase full-stack ML engineering capabilities!

cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Configure Environment
```bash
cp .env.example .env

# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Edit .env and set:
# SECRET_KEY=(paste generated key)
# DEMO_MODE=False  (for full functionality)
```

#### Run Backend Services

**Terminal 1 - API Server:**
```bash
cd backend
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

**Terminal 2 - Celery Worker:**
```bash
cd backend
source venv/bin/activate
celery -A worker.celery_app worker --loglevel=info
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will be available at `http://localhost:3000`

### 4. Test the Application

1. Open `http://localhost:3000`
2. Search for any product (e.g., "iPhone 15", "Tesla Model 3")
3. Wait 30-60 seconds for analysis to complete
4. View sentiment analysis, churn predictions, and topic insights

## Deployment Modes

### Demo Mode (Fast, Mock Data)
For online demos or testing without scraping infrastructure:

```bash
# In backend/.env
DEMO_MODE=True
```

- Uses pre-generated sample data
- Completes in ~10 seconds
- No Redis/Celery required
- Perfect for portfolio demos

### Production Mode (Full Functionality)
For real-world use with actual web scraping:

```bash
# In backend/.env
DEMO_MODE=False
```

- Scrapes real customer reviews
- Requires Redis + Celery worker
- Takes 30-90 seconds per analysis
- Provides genuine insights

## API Endpoints

### Start Analysis
```http
POST /api/analysis/analyze
Content-Type: application/json

{
  "product_name": "iPhone 15"
}
```

### Check Status
```http
GET /api/analysis/{analysis_id}/status
```

### Get Dashboard Data
```http
GET /api/analysis/{product_name}/dashboard
```

Full API documentation: `http://localhost:8000/docs`

## Machine Learning Models

### Sentiment Analysis
- **Model**: DistilBERT (distilbert-base-uncased-finetuned-sst-2-english)
- **Task**: 3-class sentiment classification (positive/negative/neutral)
- **Accuracy**: ~92% on SST-2 benchmark

### Churn Prediction
- **Algorithm**: XGBoost with sentiment features
- **Features**: Average sentiment, negative ratio, comment volatility
- **Output**: Churn probability (0-1)

## License

MIT License - feel free to use this code for your own projects!

---

**Built with ❤️ by Amir Hossein Nasserpour**

For questions or collaboration: amirtashdid99@gmail.com | [@R00T99](https://t.me/R00T99)
