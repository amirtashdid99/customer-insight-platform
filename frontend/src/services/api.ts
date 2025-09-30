import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface AnalysisRequest {
  product_name: string;
}

export interface AnalysisJobResponse {
  message: string;
  analysis_id: number;
  status: string;
  estimated_time_seconds: number;
}

export interface AnalysisStatus {
  id: number;
  product_id: number;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  total_comments: number;
  avg_sentiment_score: number | null;
  positive_count: number;
  negative_count: number;
  neutral_count: number;
  churn_risk_score: number | null;
  error_message: string | null;
  created_at: string;
  completed_at: string | null;
}

export interface Comment {
  id: number;
  text: string;
  source: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  sentiment_score: number;
  confidence: number;
  author: string | null;
  scraped_at: string;
}

export interface Topic {
  id: number;
  name: string;
  mention_count: number;
  avg_sentiment: number;
  keywords: string | null;
}

export interface DashboardData {
  product: {
    id: number;
    name: string;
    created_at: string;
  };
  latest_analysis: AnalysisStatus | null;
  recent_comments: Comment[];
  topics: Topic[];
  sentiment_distribution: {
    positive: number;
    negative: number;
    neutral: number;
  };
  risk_level: string | null;
}

export const apiService = {
  startAnalysis: (data: AnalysisRequest) =>
    api.post<AnalysisJobResponse>('/api/analysis/analyze', data),
  
  getAnalysisStatus: (analysisId: number) =>
    api.get<AnalysisStatus>(`/api/analysis/status/${analysisId}`),
  
  getDashboardData: (productName: string) =>
    api.get<DashboardData>(`/api/analysis/dashboard/${productName}`),
};

export default api;
