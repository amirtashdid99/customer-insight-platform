import React, { useState } from 'react';
import './App.css';
import { apiService, DashboardData } from './services/api';
import Dashboard from './components/Dashboard';

function App() {
  const [productName, setProductName] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysisStatus, setAnalysisStatus] = useState<string>('');
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [error, setError] = useState<string>('');

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!productName.trim()) {
      setError('Please enter a product name');
      return;
    }

    setError('');
    setLoading(true);
    setDashboardData(null);
    setAnalysisStatus('Starting analysis...');

    try {
      // Start analysis
      const { data: jobResponse } = await apiService.startAnalysis({
        product_name: productName.trim()
      });

      setAnalysisStatus(`Analysis started! ID: ${jobResponse.analysis_id}`);

      // Poll for completion
      const analysisId = jobResponse.analysis_id;
      let attempts = 0;
      const maxAttempts = 30; // 1 minute max (30 attempts * 2 seconds)

      const pollInterval = setInterval(async () => {
        attempts++;

        try {
          const { data: status } = await apiService.getAnalysisStatus(analysisId);
          
          setAnalysisStatus(`Status: ${status.status.toUpperCase()} - ${status.total_comments} comments processed`);

          if (status.status === 'completed') {
            clearInterval(pollInterval);
            
            // Fetch dashboard data
            const { data: dashboard } = await apiService.getDashboardData(productName.trim());
            setDashboardData(dashboard);
            setLoading(false);
            setAnalysisStatus('');
          } else if (status.status === 'failed') {
            clearInterval(pollInterval);
            setError(status.error_message || 'Analysis failed');
            setLoading(false);
            setAnalysisStatus('');
          }
        } catch (err) {
          console.error('Polling error:', err);
        }

        if (attempts >= maxAttempts) {
          clearInterval(pollInterval);
          setError('Analysis timed out. Please try again.');
          setLoading(false);
          setAnalysisStatus('');
        }
      }, 2000); // Poll every 2 seconds

    } catch (err: any) {
      console.error('Search error:', err);
      setError(err.response?.data?.detail || 'Failed to start analysis. Make sure the backend is running.');
      setLoading(false);
      setAnalysisStatus('');
    }
  };

  return (
    <div className="App">
      <div className="container">
        <header className="header">
          <h1>Customer Insight Platform</h1>
          <p>AI-Powered Sentiment Analysis & Churn Prediction</p>
        </header>

        <div className="search-section">
          <form onSubmit={handleSearch} className="search-form">
            <input
              type="text"
              className="search-input"
              placeholder="Enter product or company name (e.g., iPhone 17, Tesla, Netflix)"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              disabled={loading}
            />
            <button 
              type="submit" 
              className="search-button"
              disabled={loading}
            >
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          </form>
        </div>

        {error && (
          <div className="error">
            <strong>Error:</strong> {error}
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <h3>{analysisStatus}</h3>
            <p>This may take up to 60 seconds...</p>
          </div>
        )}

        {dashboardData && !loading && (
          <Dashboard data={dashboardData} />
        )}

        {!dashboardData && !loading && !error && (
          <div className="card">
            <div className="empty-state">
              <div className="empty-state-icon">🔍</div>
              <h3>Get Started</h3>
              <p>Enter a product or company name to analyze customer sentiment and predict churn risk</p>
              <p style={{ marginTop: '20px', fontSize: '0.9rem', color: '#9ca3af' }}>
                <strong>Examples:</strong> iPhone 17, Tesla Model 3, Netflix, Amazon Prime, Spotify
              </p>
            </div>
          </div>
        )}

        <footer className="footer">
          <div className="footer-content">
            <div className="footer-section">
              <h3>Customer Insight Platform</h3>
              <p>Full-stack ML-powered sentiment analysis platform</p>
            </div>
            <div className="footer-section">
              <h3>Developer</h3>
              <p><strong>Amir Hossein Nasserpour</strong></p>
              <div className="contact-links">
                <a href="mailto:amirtashdid99@gmail.com" className="contact-link">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                  </svg>
                  amirtashdid99@gmail.com
                </a>
                <a href="https://t.me/R00T99" target="_blank" rel="noopener noreferrer" className="contact-link">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z"/>
                  </svg>
                  @R00T99
                </a>
              </div>
            </div>
            <div className="footer-section">
              <h3>Tech Stack</h3>
              <p>React • TypeScript • FastAPI • Celery</p>
              <p>PyTorch • Transformers • Redis • SQLite</p>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2025 Amir Hossein Nasserpour. All rights reserved.</p>
          </div>
        </footer>
      </div>
    </div>
  );
}

export default App;
