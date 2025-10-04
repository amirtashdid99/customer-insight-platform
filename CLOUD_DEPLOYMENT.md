# ☁️ Cloud Integration & AWS Deployment Guide

## Overview

This guide shows how to deploy your Customer Insight Platform using modern cloud architecture with:

- **AWS Lambda** for serverless scraping
- **AWS S3** for data storage
- **AWS RDS** for PostgreSQL database
- **AWS EventBridge** for scheduling
- **AWS SES** for email notifications

---

## 🏗️ Architecture: Cloud-Native Version

```
┌─────────────────┐
│   React App     │ (Vercel)
│   (Frontend)    │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  FastAPI Backend│ (AWS Lambda + API Gateway)
│  (REST API)     │
└────────┬────────┘
         │
    ┌────┴─────┬─────────────┬──────────────┐
    ▼          ▼             ▼              ▼
┌────────┐    ┌────────┐  ┌────────────┐  ┌───────┐
│AWS RDS │    │AWS S3    │  │Lambda      │  │AWS SES│
│(PostgreSQL) │(Raw Data)│(Scraping) │ │(Email)│
└────────┘    └────────┘  └────────────┘  └───────┘
                             ▲
                             │ Trigger
                        ┌────┴─────┐
                        │EventBridge│
                        │(Scheduler)│
                        └──────────┘
```

---

## 🚀 Deployment Option 1: AWS Serverless

### Step 1: Set Up AWS RDS PostgreSQL

1. **Go to AWS RDS Console**
2. **Create Database**:
   - Engine: PostgreSQL 15
   - Template: Free tier (or Production)
   - DB instance identifier: `customer-insight-db`
   - Master username: `postgres`
   - Master password: <generate-strong-password>
   - DB instance class: `db.t3.micro` (free tier)
   - Storage: 20 GB
   - Public access: Yes (for testing)
   - VPC security group: Create new → Allow inbound 5432

3. **Get Connection String**:
   ```
   postgresql://postgres:<password>@customer-insight-db.xxx.us-east-1.rds.amazonaws.com:5432/postgres
   ```

### Step 2: Set Up S3 Bucket for Data Storage

```bash
# Create bucket
aws s3 mb s3://customer-insight-data --region us-east-1

# Create folder structure
aws s3api put-object --bucket customer-insight-data --key raw-data/
aws s3api put-object --bucket customer-insight-data --key processed-data/
```

**Bucket Structure:**
```
customer-insight-data/
├── raw-data/
│   └── 2025-10-04/
│       └── iphone-15/
│           └── comments.json
└── processed-data/
    └── 2025-10-04/
        └── iphone-15/
            ├── sentiment.json
            └── analysis.json
```

### Step 3: Deploy Backend to AWS Lambda

#### Install Mangum (Lambda Adapter)

```bash
cd backend
pip install mangum
```

#### Update `main.py` for Lambda

```python
# backend/app/main.py
from mangum import Mangum

# ... existing FastAPI app code ...

# Add Lambda handler
lambda_handler = Mangum(app, lifespan="off")
```

#### Create Lambda Deployment Package

```bash
# Create deployment package
cd backend
pip install -r requirements.txt -t ./package
cd package
zip -r ../deployment.zip .
cd ..
zip -r deployment.zip app/
```

#### Deploy via AWS Console

1. **Go to Lambda Console**
2. **Create Function**:
   - Name: `customer-insight-api`
   - Runtime: Python 3.11
   - Architecture: x86_64
   - Memory: 1024 MB (for ML models)
   - Timeout: 30 seconds
3. **Upload Code**: Upload `deployment.zip`
4. **Set Environment Variables**:
   ```
   DATABASE_URL=postgresql://postgres:xxx@xxx.rds.amazonaws.com:5432/postgres
   SECRET_KEY=<your-secret-key>
   DEMO_MODE=False
   AWS_S3_BUCKET=customer-insight-data
   ```
5. **Add Lambda Layer** (for heavy dependencies):
   - PyTorch/Transformers: Use pre-built layers or create custom

#### Create API Gateway

1. **Go to API Gateway Console**
2. **Create REST API**
3. **Create Resource**: `/{proxy+}`
4. **Create Method**: ANY
5. **Integration**: Lambda Function → `customer-insight-api`
6. **Deploy API**: Stage `prod`
7. **Get Invoke URL**: `https://xxx.execute-api.us-east-1.amazonaws.com/prod`

### Step 4: Deploy Scraper as Separate Lambda

Create `scraper_lambda.py`:

```python
import json
import boto3
from datetime import datetime
from app.scrapers import create_scraper

s3 = boto3.client('s3')
BUCKET = 'customer-insight-data'

def lambda_handler(event, context):
    """
    Serverless scraper function
    
    Event format:
    {
        "product_name": "iPhone 15",
        "max_results": 50
    }
    """
    product_name = event.get('product_name')
    max_results = event.get('max_results', 50)
    
    # Scrape data
    scraper = create_scraper()
    comments = scraper.scrape_all(product_name, max_results)
    
    # Save to S3
    date_str = datetime.now().strftime('%Y-%m-%d')
    product_slug = product_name.lower().replace(' ', '-')
    key = f'raw-data/{date_str}/{product_slug}/comments.json'
    
    data = [comment.dict() for comment in comments]
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(data),
        ContentType='application/json'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Scraped {len(comments)} comments',
            's3_key': key
        })
    }
```

**Deploy:**
```bash
zip scraper.zip scraper_lambda.py
aws lambda create-function \
  --function-name customer-insight-scraper \
  --runtime python3.11 \
  --role arn:aws:iam::xxx:role/lambda-execution-role \
  --handler scraper_lambda.lambda_handler \
  --zip-file fileb://scraper.zip \
  --timeout 300 \
  --memory-size 512
```

### Step 5: Set Up EventBridge Scheduler

Schedule scraper to run every 6 hours:

1. **Go to EventBridge Console**
2. **Create Rule**:
   - Name: `customer-insight-scraper-schedule`
   - Schedule: `rate(6 hours)`
   - Target: Lambda function → `customer-insight-scraper`
   - Input:
     ```json
     {
       "product_name": "iPhone 15",
       "max_results": 50
     }
     ```

### Step 6: Configure AWS SES for Emails

```bash
# Verify email identity
aws ses verify-email-identity --email-address your-email@gmail.com

# Update backend env
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USERNAME=<AWS-SES-SMTP-USERNAME>
EMAIL_PASSWORD=<AWS-SES-SMTP-PASSWORD>
```

---

## 🚀 Deployment Option 2: Azure Cloud

### Azure Services Used

- **Azure Functions** for serverless compute
- **Azure Blob Storage** for data storage
- **Azure Database for PostgreSQL** for database
- **Azure Logic Apps** for orchestration
- **SendGrid** for email

### Quick Setup

```bash
# Install Azure CLI
az login

# Create Resource Group
az group create --name customer-insight-rg --location eastus

# Create PostgreSQL
az postgres flexible-server create \
  --resource-group customer-insight-rg \
  --name customer-insight-db \
  --admin-user myadmin \
  --admin-password <SecurePassword123!> \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32

# Create Storage Account
az storage account create \
  --name customerinsightdata \
  --resource-group customer-insight-rg \
  --location eastus \
  --sku Standard_LRS

# Create Container
az storage container create \
  --name raw-data \
  --account-name customerinsightdata
```

---

## 🚀 Deployment Option 3: Google Cloud Platform

### GCP Services Used

- **Cloud Run** for containerized API
- **Cloud Storage** for data storage
- **Cloud SQL** for PostgreSQL
- **Cloud Scheduler** for cron jobs
- **SendGrid** for email

### Quick Setup

```bash
# Enable APIs
gcloud services enable run.googleapis.com sql-component.googleapis.com

# Create Cloud SQL instance
gcloud sql instances create customer-insight-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create customer_insight --instance=customer-insight-db

# Deploy to Cloud Run
gcloud run deploy customer-insight-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 📊 Cost Comparison

### Free Tier Limits

| Provider | Compute | Database | Storage |
|----------|---------|----------|---------|
| **AWS** | 1M Lambda requests/month | 750 hrs/month RDS | 5 GB S3 |
| **Azure** | 1M Function executions/month | 750 hrs/month PostgreSQL | 5 GB Blob Storage |
| **GCP** | 2M Cloud Run requests/month | Not free | 5 GB Storage |
| **Render** | 750 hrs/month (sleeps) | 512 MB RAM | N/A |

### Estimated Monthly Costs (After Free Tier)

**Low Traffic (< 10K requests/month):**
- AWS: ~$15-20
- Azure: ~$12-18
- GCP: ~$10-15
- Render: $0 (free tier)

**Medium Traffic (100K requests/month):**
- AWS: ~$50-80
- Azure: ~$45-70
- GCP: ~$40-65
- Render: $7 (paid tier)

---

## 🔧 Environment Configuration

### AWS Lambda Environment Variables

```bash
DATABASE_URL=postgresql://user:pass@xxx.rds.amazonaws.com:5432/dbname
SECRET_KEY=your-super-secret-key-min-32-chars
DEMO_MODE=False
AWS_S3_BUCKET=customer-insight-data
AWS_REGION=us-east-1
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USERNAME=<SES-SMTP-USERNAME>
EMAIL_PASSWORD=<SES-SMTP-PASSWORD>
FRONTEND_URL=https://customer-insight-platform.vercel.app
```

---

## 📈 Monitoring & Logging

### AWS CloudWatch

```python
import boto3
import logging

cloudwatch = boto3.client('logs')
logger = logging.getLogger()

def log_to_cloudwatch(log_group, log_stream, message):
    cloudwatch.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[{
            'timestamp': int(time.time() * 1000),
            'message': message
        }]
    )
```

### Metrics Dashboard

Track:
- API response times
- Lambda invocations
- Database connections
- Error rates
- Scraping success rate

---

## 🎯 Benefits of Cloud Deployment

### AWS Lambda Advantages

✅ **No Server Management** - AWS handles scaling  
✅ **Pay Per Use** - Only pay for actual compute time  
✅ **Auto Scaling** - Handles traffic spikes automatically  
✅ **99.99% Uptime SLA** - Highly available  
✅ **Global CDN** - Fast response worldwide  

### Data Pipeline Benefits

✅ **Decoupled Architecture** - Scraper, API, ML models separate  
✅ **Scalable** - Process millions of comments  
✅ **Fault Tolerant** - Failures don't crash entire system  
✅ **Auditable** - All raw data preserved in S3  
✅ **Reprocessable** - Rerun analysis on historical data  

---

## 🔐 Security Best Practices

### IAM Roles

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::customer-insight-data/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

### Secrets Management

Use AWS Secrets Manager:

```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
db_credentials = get_secret('customer-insight/database')
DATABASE_URL = db_credentials['connection_string']
```

---

## 📚 Additional Resources

- **AWS Lambda Python**: https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html
- **Mangum (FastAPI on Lambda)**: https://mangum.io/
- **AWS RDS**: https://aws.amazon.com/rds/postgresql/
- **EventBridge**: https://docs.aws.amazon.com/eventbridge/
- **AWS SES**: https://docs.aws.amazon.com/ses/

---

## 🎉 Summary

You now have multiple cloud deployment options:

1. **Render (Current)** - Simple, free tier, great for demos
2. **AWS Lambda** - Serverless, scalable, production-ready
3. **Azure Functions** - Microsoft cloud alternative
4. **GCP Cloud Run** - Google cloud alternative

**Choose based on:**
- Budget
- Traffic expectations
- Team expertise
- Regional requirements

All options support the new authentication and notification features! 🚀
