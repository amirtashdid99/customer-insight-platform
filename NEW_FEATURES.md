# 🎉 New Features: User Accounts & Smart Alerts

## Overview

Your Customer Insight Platform now includes **three powerful enterprise features** that make it stand out:

1. **🔐 User Authentication** - Secure account system
2. **📧 Email Alerts** - Automated sentiment spike notifications
3. **⭐ Saved Products** - Track and manage favorite products

---

## 🔐 Feature 1: User Authentication

### What It Does

Users can register accounts, log in, and access personalized features.

### API Endpoints

#### Register New User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2025-10-04T10:00:00Z"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepass123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Get Current User Info
```http
GET /api/auth/me
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "last_login": "2025-10-04T10:05:00Z"
}
```

### Security Features

- ✅ **Bcrypt Password Hashing** - Passwords never stored in plain text
- ✅ **JWT Tokens** - Secure, stateless authentication
- ✅ **30-minute Token Expiry** - Auto logout for security
- ✅ **Email Validation** - Pydantic EmailStr validation

---

## 📧 Feature 2: Email Alerts

### What It Does

Automatically sends email notifications when significant sentiment changes are detected:

- **Negative Spike Alert** - When negative sentiment increases by >20%
- **Positive Surge Alert** - When positive sentiment increases by >30%

### Setup Email (Optional)

Add to `backend/.env`:

```bash
# Email Settings (Optional - for alerts)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password  # Generate from Google Account

# Frontend URL (for email links)
FRONTEND_URL=https://customer-insight-platform.vercel.app
```

**Generate Gmail App Password:**
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" → "Other (Custom name)" → "Customer Insight Platform"
3. Copy the 16-character password
4. Paste in `.env` as `EMAIL_PASSWORD`

### API Endpoints

#### Enable Notifications for a Product
```http
POST /api/notifications/preferences
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_name": "iPhone 15",
  "email_alerts": true,
  "sentiment_threshold": 0.2
}
```

**Response:**
```json
{
  "message": "Notification preferences created",
  "product_name": "iPhone 15",
  "email_alerts": true
}
```

#### Get Notification Preferences
```http
GET /api/notifications/preferences/iPhone%2015
Authorization: Bearer <token>
```

**Response:**
```json
{
  "product_name": "iPhone 15",
  "email_alerts": true,
  "sentiment_threshold": 0.2
}
```

### How Alerts Work

1. **Analysis Completes** - Backend finishes analyzing product
2. **Spike Detection** - System compares with previous analysis
3. **Email Sent** - If spike detected, email sent to subscribed users
4. **Beautiful HTML Email** - Professional format with dashboard link

**Example Alert Email:**

```
⚠️ Negative Sentiment Alert

Hello John Doe,

We detected a significant increase in negative sentiment for iPhone 15:

• Negative sentiment increased by 25.3%
• Current: 45.8% negative
• Previous: 20.5% negative

⚠️ Recommendation: Review recent customer feedback immediately and address concerns.

[View Dashboard Button]
```

---

## ⭐ Feature 3: Saved Products

### What It Does

Users can save products to their personal dashboard and track them over time.

### API Endpoints

#### Save a Product
```http
POST /api/saved-products/
Authorization: Bearer <token>
Content-Type: application/json

{
  "product_name": "iPhone 15",
  "nickname": "Main Product",
  "notes": "Track competitors"
}
```

**Response:**
```json
{
  "id": 1,
  "product_name": "iPhone 15",
  "nickname": "Main Product",
  "notes": "Track competitors",
  "created_at": "2025-10-04T10:00:00Z",
  "last_analysis": "2025-10-04T09:45:00Z",
  "latest_sentiment": "positive"
}
```

#### Get All Saved Products
```http
GET /api/saved-products/
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "product_name": "iPhone 15",
    "nickname": "Main Product",
    "notes": "Track competitors",
    "created_at": "2025-10-04T10:00:00Z",
    "last_analysis": "2025-10-04T09:45:00Z",
    "latest_sentiment": "positive"
  },
  {
    "id": 2,
    "product_name": "Tesla Model 3",
    "nickname": null,
    "notes": null,
    "created_at": "2025-10-03T15:20:00Z",
    "last_analysis": "2025-10-04T08:30:00Z",
    "latest_sentiment": "mixed"
  }
]
```

#### Remove Saved Product
```http
DELETE /api/saved-products/1
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Removed iPhone 15 from saved products"
}
```

---

## 🗄️ Database Updates

New tables added:

### `users` Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

### `notification_preferences` Table
```sql
CREATE TABLE notification_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    email_alerts BOOLEAN DEFAULT TRUE,
    sentiment_threshold FLOAT DEFAULT 0.2,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP
);
```

### `saved_products` Table
```sql
CREATE TABLE saved_products (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    nickname VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🚀 Deployment Notes

### Environment Variables

Add to Render:

```bash
# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Frontend URL
FRONTEND_URL=https://customer-insight-platform.vercel.app
```

### Database Migration

After deployment, database tables auto-create on first run.

Or manually migrate:
```bash
cd backend
alembic revision --autogenerate -m "Add user authentication and notifications"
alembic upgrade head
```

---

## 📱 Frontend Integration (Optional)

### Login Component Example

```typescript
// Login.tsx
const handleLogin = async (email: string, password: string) => {
  const formData = new FormData();
  formData.append('username', email);  // OAuth2 uses 'username' field
  formData.append('password', password);
  
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  
  // Save token
  localStorage.setItem('token', data.access_token);
  
  // Use in subsequent requests
  const headers = {
    'Authorization': `Bearer ${data.access_token}`
  };
};
```

### Authenticated API Calls

```typescript
const apiWithAuth = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to all requests
apiWithAuth.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Save product
const saveProduct = async (productName: string) => {
  const response = await apiWithAuth.post('/api/saved-products/', {
    product_name: productName
  });
  return response.data;
};
```

---

## ✅ Testing

### Test Authentication

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "Test User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123"

# Get user info (use token from login response)
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <your-token>"
```

### Test Saved Products

```bash
TOKEN="<your-token>"

# Save a product
curl -X POST http://localhost:8000/api/saved-products/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "iPhone 15",
    "nickname": "Main Product"
  }'

# Get saved products
curl -X GET http://localhost:8000/api/saved-products/ \
  -H "Authorization: Bearer $TOKEN"
```

### Test Notifications

```bash
# Enable alerts
curl -X POST http://localhost:8000/api/notifications/preferences \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "iPhone 15",
    "email_alerts": true,
    "sentiment_threshold": 0.2
  }'

# Get preferences
curl -X GET "http://localhost:8000/api/notifications/preferences/iPhone%2015" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🎯 Benefits for Your Portfolio

These features showcase:

1. **Full-Stack Skills** - Complete authentication flow
2. **Security Best Practices** - JWT, bcrypt, proper validation
3. **Email Integration** - SMTP, HTML emails, async tasks
4. **User Experience** - Personalized dashboards, alerts
5. **Database Design** - Relationships, constraints, migrations
6. **API Design** - RESTful, well-documented endpoints
7. **Enterprise Features** - Multi-user, notifications, saved items

---

## 🔮 Future Enhancements

Potential additions:

- **WebSocket Real-Time Updates** - Live dashboard updates
- **Slack/Discord Webhooks** - Team notifications
- **Admin Dashboard** - User management interface
- **API Rate Limiting** - Prevent abuse
- **Email Verification** - Confirm user emails
- **Password Reset** - Forgot password flow
- **OAuth2 Social Login** - Google, GitHub login
- **Scheduled Reports** - Daily/weekly email summaries

---

## 📚 Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **FastAPI Security**: https://fastapi.tiangolo.com/tutorial/security/

---

## 🎉 Summary

You now have a **professional-grade platform** with:

✅ User authentication & authorization  
✅ Smart sentiment alert system  
✅ Personal product tracking  
✅ Email notifications  
✅ Enterprise-ready features

**Ready to deploy and impress!** 🚀
