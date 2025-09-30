import React from 'react';
import { DashboardData } from '../services/api';
import SentimentChart from './SentimentChart';

interface DashboardProps {
  data: DashboardData;
}

const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  const { product, latest_analysis, recent_comments, topics, sentiment_distribution, risk_level } = data;

  if (!latest_analysis) {
    return (
      <div className="card">
        <div className="empty-state">
          <p>No analysis data available yet.</p>
        </div>
      </div>
    );
  }

  const getRiskColor = (risk: string | null) => {
    if (!risk) return 'low';
    return risk.toLowerCase();
  };

  const getSentimentEmoji = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return '😊';
      case 'negative': return '😞';
      default: return '😐';
    }
  };

  return (
    <div className="dashboard">
      {/* Overview Metrics */}
      <div className="card">
        <h2>📊 Analysis Overview - {product.name}</h2>
        <div className="metrics-grid">
          <div className="metric-card">
            <p className="metric-value">{latest_analysis.total_comments}</p>
            <p className="metric-label">Total Comments</p>
          </div>
          <div className="metric-card positive">
            <p className="metric-value">{latest_analysis.positive_count}</p>
            <p className="metric-label">Positive ({sentiment_distribution.positive}%)</p>
          </div>
          <div className="metric-card negative">
            <p className="metric-value">{latest_analysis.negative_count}</p>
            <p className="metric-label">Negative ({sentiment_distribution.negative}%)</p>
          </div>
          <div className="metric-card neutral">
            <p className="metric-value">{latest_analysis.neutral_count}</p>
            <p className="metric-label">Neutral ({sentiment_distribution.neutral}%)</p>
          </div>
        </div>

        <div style={{ marginTop: '20px' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#2d3748' }}>
            Churn Risk Assessment
          </h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <span className={`risk-badge ${getRiskColor(risk_level)}`}>
              {risk_level || 'Unknown'} Risk
            </span>
            <span style={{ color: '#6b7280' }}>
              Probability: {((latest_analysis.churn_risk_score || 0) * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      </div>

      {/* Sentiment Chart */}
      <div className="card">
        <h2>📈 Sentiment Distribution</h2>
        <SentimentChart distribution={sentiment_distribution} />
      </div>

      {/* Topics */}
      {topics.length > 0 && (
        <div className="card">
          <h2>🏷️ Key Topics</h2>
          <div className="topics-grid">
            {topics.map((topic) => (
              <div key={topic.id} className="topic-item">
                <span className="topic-name">{topic.name}</span>
                <div className="topic-stats">
                  <span className="topic-mentions">
                    {topic.mention_count} mentions
                  </span>
                  <span className={`topic-sentiment ${topic.avg_sentiment > 0 ? 'positive' : 'negative'}`}>
                    {topic.avg_sentiment > 0 ? '👍' : '👎'} {topic.avg_sentiment.toFixed(2)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Comments */}
      <div className="card">
        <h2>💬 Recent Comments ({recent_comments.length})</h2>
        <div className="comment-list">
          {recent_comments.map((comment) => (
            <div key={comment.id} className={`comment-item ${comment.sentiment}`}>
              <div className="comment-header">
                <span>
                  {getSentimentEmoji(comment.sentiment)} {comment.source}
                  {comment.author && ` • ${comment.author}`}
                </span>
                <span className={`sentiment-badge ${comment.sentiment}`}>
                  {comment.sentiment}
                </span>
              </div>
              <p className="comment-text">{comment.text}</p>
              <div style={{ marginTop: '8px', fontSize: '0.8rem', color: '#9ca3af' }}>
                Score: {comment.sentiment_score.toFixed(2)} | 
                Confidence: {(comment.confidence * 100).toFixed(1)}%
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
