# Customer Insight Platform - Frontend

This is the React + TypeScript frontend for the Customer Insight Platform.

## Features

- 🔍 **Product Search** - Analyze any product or company
- 📊 **Interactive Dashboard** - Beautiful data visualizations
- 💬 **Comment Analysis** - View sentiment-analyzed customer comments
- 🏷️ **Topic Extraction** - See what customers talk about
- ⚠️ **Risk Assessment** - Churn prediction with visual indicators
- 📈 **Real-time Updates** - Live polling of analysis status

## Tech Stack

- **React 18** with TypeScript
- **Recharts** for data visualization
- **Axios** for API calls
- **Modern CSS** with gradients and animations

## Setup

### Prerequisites

Make sure you have Node.js 16+ installed:
```powershell
node --version
```

If not installed, download from: https://nodejs.org/

### Installation

```powershell
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The app will open at http://localhost:3000

### Environment Variables

Create a `.env` file (already created) with:
```
REACT_APP_API_URL=http://localhost:8000
```

## Usage

1. **Make sure the backend is running** on http://localhost:8000
2. **Start the frontend**: `npm start`
3. **Enter a product name** (e.g., "iPhone 15", "Tesla")
4. **Click "Analyze"** and wait for results (~60 seconds)
5. **Explore the dashboard** with sentiment charts, comments, and topics

## Project Structure

```
src/
├── components/
│   ├── Dashboard.tsx          # Main dashboard component
│   └── SentimentChart.tsx     # Pie chart for sentiment distribution
├── services/
│   └── api.ts                 # API service and TypeScript interfaces
├── App.tsx                    # Main application component
├── App.css                    # Application styles
├── index.tsx                  # Entry point
└── index.css                  # Global styles
```

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000` and uses three main endpoints:

1. `POST /api/analysis/analyze` - Start analysis
2. `GET /api/analysis/status/{id}` - Check analysis status
3. `GET /api/analysis/dashboard/{product_name}` - Get results

## Building for Production

```powershell
npm run build
```

This creates an optimized production build in the `build/` directory.

## Customization

### Change Colors

Edit the gradient in `src/index.css`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Modify Polling Interval

In `src/App.tsx`, change the polling interval (default 2 seconds):
```typescript
}, 2000); // Poll every 2 seconds
```

### Add More Charts

Install additional Recharts components and add them to the Dashboard!

## Troubleshooting

### "Failed to start analysis"
- Make sure the backend is running on http://localhost:8000
- Check CORS settings in backend allow http://localhost:3000

### Port 3000 already in use
```powershell
# Use a different port
set PORT=3001 && npm start
```

### Module not found errors
```powershell
# Reinstall dependencies
rm -rf node_modules
npm install
```

## Next Steps

- [ ] Add authentication
- [ ] Implement saved searches
- [ ] Add more chart types (bar charts, line charts for trends)
- [ ] Add export to CSV/PDF
- [ ] Implement dark mode toggle
- [ ] Add historical comparison

---

**This frontend completes your full-stack application!** 🎉
