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
          <h1>🎯 Customer Insight Platform</h1>
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
      </div>
    </div>
  );
}

export default App;
