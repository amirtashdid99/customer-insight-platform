# 🏗️ System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (React + TypeScript)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Search     │  │  Dashboard   │  │   Metrics    │           │
│  │   Input      │  │   View       │  │   Charts     │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTP/REST API
                          │ (Axios)
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API LAYER (FastAPI)                        │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  POST /api/analysis/analyze                            │     │
│  │  GET  /api/analysis/status/{id}                        │     │
│  │  GET  /api/analysis/dashboard/{product_name}           │     │
│  └────────────────────────────────────────────────────────┘     │
│                          │                                      │
│         ┌────────────────┼────────────────┐                     │
│         ▼                ▼                ▼                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
│  │ Analysis │    │  Scraper │    │    ML    │                   │
│  │ Pipeline │◄───┤  Service │───►│  Models  │                   │
│  └──────────┘    └──────────┘    └──────────┘                │
└─────────────────────────┬───────────────────────────────────────┘
                          │ SQLAlchemy ORM
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  DATABASE (PostgreSQL)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  products   │  │  analyses   │  │  comments   │              │
│  │  ──────────│  │  ──────────│  │  ──────────│                 │
│  │  id         │  │  id         │  │  id         │              │
│  │  name       │  │  product_id │  │  text       │              │
│  │  created_at │  │  status     │  │  sentiment  │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                         └──────────────┬──────────┘             │
│                                        │                        │
│                                  ┌─────────────┐                │
│                                  │   topics    │                │
│                                  │  ──────────│                 │
│                                  │  id         │                │
│                                  │  name       │                │
│                                  └─────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Complete Analysis Pipeline

```
┌──────────┐
│  User    │
│ enters   │  1. User enters product name
│ product  │     "iPhone 15"
│  name    │
└────┬─────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ POST /api/analysis/analyze              │  2. API creates analysis job
│                                         │     Status: PENDING
│ • Create/Find Product in DB             │     Returns: analysis_id
│ • Create Analysis record                │
│ • Start background task                 │
│ • Return immediately                    │
└────┬────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ Background Task: run_analysis_job()     │  3. Background processing begins
│                                         │     Status: IN_PROGRESS
│ Status → IN_PROGRESS                    │
└────┬────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ Step 1: Web Scraping                    │  4. Scrape from multiple sources
│                                         │
│ ┌──────────────────────────────────────┤
│ │ Reddit Scraper (async)               │     • 40% of quota
│ │  ├─ Search for product mentions      │
│ │  ├─ Extract comments                 │
│ │  └─ Parse metadata                   │
│ ├──────────────────────────────────────┤
│ │ Review Site Scraper (async)          │     • 30% of quota
│ │  ├─ Trustpilot/G2 style              │
│ │  ├─ Extract reviews                  │
│ │  └─ Parse ratings                    │
│ ├──────────────────────────────────────┤
│ │ Twitter Scraper (async)              │     • 30% of quota
│ │  ├─ Search tweets                    │
│ │  ├─ Extract text                     │
│ │  └─ Parse metadata                   │
│ └──────────────────────────────────────┘
│
│ Result: 50 Comment objects
└────┬────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ Step 2: Sentiment Analysis              │  5. Analyze each comment
│                                         │
│ Input: 50 comment texts                 │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Sentiment Analyzer (DistilBERT)     │ │     • Batch processing
│ │                                     │ │     • GPU accelerated (if available)
│ │ Text → Tokenizer → Model → Output   │ │     • ~512 chars per comment
│ │                                     │ │
│ │ For each comment:                   │ │
│ │  • sentiment: "positive"|"negative" │ │
│ │  • score: -1.0 to 1.0               │ │
│ │  • confidence: 0.0 to 1.0           │ │
│ └─────────────────────────────────────┘ │
│
│ Result: 50 sentiment predictions
└────┬────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ Step 3: Database Storage                │  6. Save all data
│                                         │
│ For each comment:                       │
│  INSERT INTO customer_comments          │
│   (text, source, sentiment,             │
│    sentiment_score, confidence, ...)    │
│                                         │
│ Result: 50 rows in customer_comments    │
└────┬────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ Step 4: Aggregate Metrics               │  7. Calculate statistics
│                                         │
│ • Total comments: 50                    │
│ • Positive: 30 (60%)                    │
│ • Negative: 12 (24%)                    │
│ • Neutral: 8 (16%)                      │
│ • Avg sentiment: 0.35                   │
│ • Sentiment volatility: 0.42            │
└────┬────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ Step 5: Churn Prediction                │  8. Predict churn risk
│                                         │
│ Input Features:                         │
│  • avg_sentiment: 0.35                  │
│  • negative_ratio: 0.24                 │
│  • total_comments: 50                   │
│  • sentiment_volatility: 0.42           │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Custom Churn Algorithm              │ │
│ │                                     │ │
│ │ sentiment_risk = (1 - avg) / 2      │ │
│ │ negative_boost = ratio * 0.3        │ │
│ │ volatility_boost = min(vol, 0.2)    │ │
│ │ volume_factor = min(count/50, 1.0)  │ │
│ │                                     │ │
│ │ churn_prob = weighted_combination   │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Result: churn_probability = 0.42        │
│         risk_level = "medium"           │
└────┬────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ Step 6: Topic Extraction                │  9. Extract key themes
│                                         │
│ Analyze all comment texts for keywords: │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Topic: "price"                      │ │     • Mentions: 15
│ │  Keywords: price, expensive, cost   │ │     • Avg sentiment: -0.2
│ ├─────────────────────────────────────┤ │
│ │ Topic: "quality"                    │ │     • Mentions: 23
│ │  Keywords: quality, reliable        │ │     • Avg sentiment: 0.6
│ ├─────────────────────────────────────┤ │
│ │ Topic: "support"                    │ │     • Mentions: 8
│ │  Keywords: support, service         │ │     • Avg sentiment: -0.4
│ └─────────────────────────────────────┘ │
│                                         │
│ INSERT INTO topics (...)                │
└────┬────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ Step 7: Finalize Analysis               │  10. Update analysis record
│                                         │
│ UPDATE analyses SET                     │
│   status = 'COMPLETED',                 │
│   total_comments = 50,                  │
│   positive_count = 30,                  │
│   negative_count = 12,                  │
│   neutral_count = 8,                    │
│   avg_sentiment_score = 0.35,           │
│   churn_risk_score = 0.42,              │
│   completed_at = NOW()                  │
│ WHERE id = analysis_id                  │
└────┬────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ Client polls: GET /status/{id}          │  11. User retrieves results
│                                         │
│ Returns: status = "COMPLETED"           │
└────┬────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│ Client fetches:                         │  12. Display dashboard
│ GET /dashboard/iPhone 15                │
│                                         │
│ Returns:                                │
│  • Product info                         │
│  • Latest analysis                      │
│  • Recent comments (20)                 │
│  • Topics (sorted by mentions)          │
│  • Sentiment distribution               │
│  • Risk level                           │
└─────────────────────────────────────────┘
```

---

## Technology Stack Details

### Frontend Layer
```
┌─────────────────────────────────────────┐
│ React 18.2+ with TypeScript             │
│                                         │
│ State Management:                       │
│  • React Hooks (useState, useEffect)    │
│  • Context API (optional for auth)      │
│                                         │
│ HTTP Client:                            │
│  • Axios with interceptors              │
│  • Async/await error handling           │
│                                         │
│ Styling:                                │
│  • Tailwind CSS 3.x                     │
│  • Responsive design utilities          │
│                                         │
│ Data Visualization:                     │
│  • Recharts (composable charts)         │
│  • Custom color schemes                 │
│                                         │
│ Routing:                                │
│  • React Router v6                      │
│  • Lazy loading components              │
└─────────────────────────────────────────┘
```

### Backend Layer
```
┌─────────────────────────────────────────┐
│ FastAPI 0.109+ (Python 3.9+)            │
│                                         │
│ API Features:                           │
│  • Automatic OpenAPI/Swagger docs       │
│  • Pydantic data validation             │
│  • Dependency injection                 │
│  • Background tasks (built-in)          │
│                                         │
│ Middleware:                             │
│  • CORS (configurable origins)          │
│  • Request logging                      │
│  • Error handling                       │
│                                         │
│ Database ORM:                           │
│  • SQLAlchemy 2.0                       │
│  • Async support (optional)             │
│  • Relationship loading strategies      │
│                                         │
│ Migrations:                             │
│  • Alembic                              │
│  • Auto-generate from models            │
│  • Version control for schema           │
└─────────────────────────────────────────┘
```

### Machine Learning Layer
```
┌─────────────────────────────────────────┐
│ Sentiment Analysis                      │
│                                         │
│ Model: DistilBERT                       │
│  • Source: Hugging Face Transformers    │
│  • Size: ~250MB                         │
│  • Speed: ~100 texts/sec (CPU)          │
│  • Accuracy: 95%+ on reviews            │
│                                         │
│ Processing:                             │
│  • Tokenization: BERT tokenizer         │
│  • Max length: 512 tokens               │
│  • Batch size: 8-32 (adaptive)          │
│  • Output: logits → softmax → sentiment │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Churn Prediction                        │
│                                         │
│ Model: XGBoost Classifier               │
│  • Training data: Telco dataset         │
│  • Features: 19 (after encoding)        │
│  • Trees: 200                           │
│  • Max depth: 5                         │
│  • ROC-AUC: 0.84+                       │
│                                         │
│ Adaptation:                             │
│  • Maps sentiment → churn features      │
│  • Custom weighted algorithm            │
│  • Considers multiple factors           │
│  • Volume-adjusted confidence           │
└─────────────────────────────────────────┘
```

### Data Layer
```
┌─────────────────────────────────────────┐
│ PostgreSQL 14+                          │
│                                         │
│ Schema Design:                          │
│  • 4 main tables                        │
│  • Foreign key constraints              │
│  • Cascade deletes                      │
│  • Indexes on frequently queried cols   │
│                                         │
│ Data Types:                             │
│  • ENUM for status/sentiment            │
│  • TIMESTAMP WITH TIMEZONE              │
│  • TEXT for unlimited length            │
│  • FLOAT for scores                     │
│                                         │
│ Performance:                            │
│  • Indexes on: product name, dates      │
│  • Efficient JOIN queries               │
│  • Connection pooling                   │
└─────────────────────────────────────────┘
```

### Web Scraping Layer
```
┌─────────────────────────────────────────┐
│ Multi-Source Scraper                    │
│                                         │
│ Libraries:                              │
│  • aiohttp (async HTTP)                 │
│  • BeautifulSoup4 (HTML parsing)        │
│  • Scrapy (optional, advanced)          │
│                                         │
│ Strategy:                               │
│  • Concurrent scraping (asyncio)        │
│  • Rate limiting (respectful)           │
│  • Error handling per source            │
│  • Timeout protection                   │
│                                         │
│ Sources (extensible):                   │
│  • Reddit (API or scraping)             │
│  • Twitter (API v2)                     │
│  • Review sites (Trustpilot, G2)        │
│  • Custom sources (easy to add)         │
└─────────────────────────────────────────┘
```

---

## Scalability Architecture

### Current (MVP)
```
Single Server:
┌─────────────────────────────┐
│  FastAPI App                │
│   • API endpoints           │
│   • Background tasks        │
│   • ML models loaded        │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  PostgreSQL                 │
│   • All data                │
└─────────────────────────────┘
```

### Scaled (Production-Ready)
```
Load Balancer
     │
     ├─────────────┬─────────────┬─────────────┐
     ▼             ▼             ▼             ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ API     │  │ API     │  │ API     │  │ API     │
│ Server  │  │ Server  │  │ Server  │  │ Server  │
└────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘
     │            │            │            │
     └────────────┴────────────┴────────────┘
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Redis   │  │ Celery  │  │ ML      │
│ Cache   │  │ Workers │  │ Service │
└─────────┘  └─────────┘  └─────────┘
                  │
                  ▼
        ┌──────────────────┐
        │ PostgreSQL       │
        │ (Primary+Replica)│
        └──────────────────┘
```

---

## Security Considerations

```
┌─────────────────────────────────────────┐
│ Current Implementation                  │
│                                         │
│ ✅ Environment variables for secrets    │
│ ✅ CORS configuration                   │
│ ✅ SQL injection protection (ORM)       │
│ ✅ Input validation (Pydantic)          │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Production Enhancements                 │
│                                         │
│ 🔒 JWT authentication                   │
│ 🔒 Rate limiting per user/IP            │
│ 🔒 API key management                   │
│ 🔒 HTTPS only                           │
│ 🔒 Database encryption at rest          │
│ 🔒 Secrets management (AWS Secrets)     │
└─────────────────────────────────────────┘
```

---

## Deployment Options

### Option 1: Traditional VPS
```
DigitalOcean/Linode Droplet
├── Nginx (reverse proxy)
├── FastAPI (via uvicorn/gunicorn)
├── PostgreSQL (same or separate server)
└── Frontend (built static files)
```

### Option 2: Container-based
```
Docker Compose:
├── backend container (FastAPI)
├── frontend container (Nginx + React build)
├── postgres container
└── redis container (optional)
```

### Option 3: Cloud Platform
```
AWS:
├── Frontend: S3 + CloudFront
├── Backend: ECS/Fargate or Lambda
├── Database: RDS PostgreSQL
└── ML Models: SageMaker or ECS

Heroku (easiest):
├── Web dyno (FastAPI)
├── Heroku Postgres addon
└── Frontend on Vercel/Netlify
```

---

This architecture provides a solid foundation that can scale from MVP to production! 🚀
