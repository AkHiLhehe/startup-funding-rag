import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface SearchRequest {
  query: string;
  query_type?: 'investor_search' | 'startup_search' | 'funding_analysis' | 'market_intelligence' | 'general';
  top_k?: number;
  include_citations?: boolean;
  response_language?: string;
  use_web_search?: boolean;
}

export interface Citation {
  source_id: string;
  source_type: string;
  source_title: string;
  source_url?: string;
  excerpt: string;
  confidence_score: number;
  published_date?: string;
}

export interface SearchResponse {
  query: string;
  answer: string;
  citations: Citation[];
  retrieved_chunks: number;
  processing_time: number;
  confidence_score: number;
  metadata: Record<string, any>;
}

export interface IngestDocumentRequest {
  content: string;
  metadata: Record<string, any>;
  document_type: string;
  source_url?: string;
}

export interface Metrics {
  total_queries: number;
  avg_processing_time_ms: number;
  avg_confidence_score: number;
  avg_retrieved_chunks: number;
  avg_citations: number;
  avg_response_length: number;
}

export const searchAPI = {
  search: async (request: SearchRequest): Promise<SearchResponse> => {
    const response = await api.post('/api/v1/search/', { ...request, use_web_search: true });
    return response.data;
  },

  searchInvestor: async (investorName: string): Promise<SearchResponse> => {
    const response = await api.get(`/api/v1/search/investor/${investorName}`);
    return response.data;
  },

  searchStartup: async (startupName: string): Promise<SearchResponse> => {
    const response = await api.get(`/api/v1/search/startup/${startupName}`);
    return response.data;
  },
};

export const ingestAPI = {
  ingestDocument: async (request: IngestDocumentRequest) => {
    const response = await api.post('/api/v1/ingest/document', request);
    return response.data;
  },

  ingestPDF: async (file: File, metadata: Record<string, any>) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('metadata', JSON.stringify(metadata));

    const response = await api.post('/api/v1/ingest/pdf', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export const analyticsAPI = {
  getMetrics: async (lastN?: number): Promise<Metrics> => {
    const response = await api.get('/api/v1/analytics/metrics', {
      params: { last_n: lastN },
    });
    return response.data;
  },

  getStatistics: async () => {
    const response = await api.get('/api/v1/analytics/statistics');
    return response.data;
  },

  getQueryHistory: async (limit: number = 100) => {
    const response = await api.get('/api/v1/analytics/queries', {
      params: { limit },
    });
    return response.data;
  },
};

export const healthAPI = {
  check: async () => {
    const response = await api.get('/api/v1/health');
    return response.data;
  },

  info: async () => {
    const response = await api.get('/api/v1/info');
    return response.data;
  },
};

export default api;
