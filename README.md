# Customer Insight Platform# Customer Insight Platform 🎯



Full-stack AI-powered customer sentiment analysis and churn prediction platform. Analyzes customer reviews from multiple sources to provide actionable business intelligence.A full-stack web application that provides real-time customer sentiment analysis and churn prediction for any product or company.



## Developer## 🚀 Features



**Amir Hossein Nasserpour**- **Real-time Data Scraping**: Fetch live customer reviews and comments from multiple sources

- Email: amirtashdid99@gmail.com- **Sentiment Analysis**: AI-powered sentiment classification (Positive/Negative/Neutral)

- Telegram: [@R00T99](https://t.me/R00T99)- **Churn Prediction**: ML-based risk assessment for customer retention

- GitHub: [@amirtashdid99](https://github.com/amirtashdid99)- **Interactive Dashboard**: Beautiful visualizations of customer insights

- **Topic Modeling**: Identify key themes in customer feedback

## Features

## 🛠️ Tech Stack

- **Multi-Source Scraping**: Aggregates reviews from Amazon, Reddit, Twitter, Trustpilot, and more

- **Sentiment Analysis**: Using DistilBERT transformer model for accurate sentiment classification### Frontend

- **Churn Prediction**: ML-powered customer churn risk assessment- React.js with TypeScript

- **Topic Extraction**: Automatic identification of key themes in customer feedback- Recharts for data visualization

- **Real-time Processing**: Async background job processing with Celery and Redis- Tailwind CSS for styling

- **Interactive Dashboard**: Beautiful data visualizations with Recharts- Axios for API calls

- **RESTful API**: FastAPI backend with automatic OpenAPI documentation

### Backend

## Tech Stack- FastAPI (Python)

- PostgreSQL database

### Backend- SQLAlchemy ORM

- **FastAPI** - Modern Python web framework- Pydantic for data validation

- **Celery** - Distributed task queue for background processing

- **Redis** - Message broker and caching### Machine Learning

- **SQLAlchemy** - SQL toolkit and ORM- Transformers (Hugging Face) for sentiment analysis

- **PyTorch & Transformers** - Deep learning for NLP- XGBoost for churn prediction

- **XGBoost** - Machine learning for churn prediction- scikit-learn for preprocessing

- **BeautifulSoup & aiohttp** - Web scraping- NLTK for text processing



### Frontend## 📁 Project Structure

- **React 18** - UI library

- **TypeScript** - Type-safe JavaScript```

- **Recharts** - Data visualizationproject1/

- **Axios** - HTTP client├── backend/                # FastAPI backend

│   ├── app/

## Project Structure│   │   ├── api/           # API endpoints

│   │   ├── models/        # Database models

```│   │   ├── ml/            # ML models & training

customer-insight-platform/│   │   ├── scrapers/      # Web scraping logic

├── backend/│   │   └── core/          # Configuration

│   ├── app/│   ├── alembic/           # Database migrations

│   │   ├── api/              # API endpoints│   └── requirements.txt

│   │   ├── core/             # Config, database, Celery├── frontend/              # React frontend

│   │   ├── models/           # Database & Pydantic models│   ├── src/

│   │   ├── ml/               # ML models (sentiment, churn)│   │   ├── components/

│   │   ├── scrapers/         # Web scraping logic│   │   ├── pages/

│   │   └── tasks/            # Celery background tasks│   │   ├── services/

│   ├── requirements.txt│   │   └── utils/

│   ├── worker.py             # Celery worker entry point│   └── package.json

│   └── .env.example└── ml_training/           # ML model training notebooks

├── frontend/    ├── notebooks/

│   ├── src/    └── datasets/

│   │   ├── components/       # React components```

│   │   ├── services/         # API client

│   │   └── App.tsx## 🎯 Current Progress

│   └── package.json

└── README.md- [x] Phase 1: Database & ML Models Setup ✅

```- [x] Phase 2: Backend API Development ✅

- [x] Phase 3: Frontend Development ✅

## Local Development Setup- [ ] Phase 4: Testing & Deployment



### Prerequisites## 🚀 Getting Started

- Python 3.9+

- Node.js 16+### Prerequisites

- Redis server- Python 3.9+

- Node.js 16+

### 1. Clone Repository- PostgreSQL 14+

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
