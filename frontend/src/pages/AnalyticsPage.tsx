import React, { useState, useEffect } from 'react';
import { analyticsAPI, Metrics } from '../services/api';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const AnalyticsPage: React.FC = () => {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [statistics, setStatistics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError(null);

    try {
      const [metricsData, statsData] = await Promise.all([
        analyticsAPI.getMetrics(),
        analyticsAPI.getStatistics(),
      ]);

      setMetrics(metricsData);
      setStatistics(statsData);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-600">Loading analytics...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          System Analytics & Metrics
        </h1>
        <p className="text-gray-600">
          Track system performance, evaluation metrics, and data statistics
        </p>
      </div>

      {/* System Statistics */}
      {statistics && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="text-sm text-gray-500 mb-1">Startups</div>
            <div className="text-3xl font-bold text-primary-600">
              {statistics.startups.toLocaleString()}
            </div>
          </div>

          <div className="card">
            <div className="text-sm text-gray-500 mb-1">Investors</div>
            <div className="text-3xl font-bold text-primary-600">
              {statistics.investors.toLocaleString()}
            </div>
          </div>

          <div className="card">
            <div className="text-sm text-gray-500 mb-1">Funding Rounds</div>
            <div className="text-3xl font-bold text-primary-600">
              {statistics.funding_rounds.toLocaleString()}
            </div>
          </div>

          <div className="card">
            <div className="text-sm text-gray-500 mb-1">Documents</div>
            <div className="text-3xl font-bold text-primary-600">
              {statistics.documents.toLocaleString()}
            </div>
          </div>
        </div>
      )}

      {/* Query Metrics */}
      {metrics && (
        <>
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="card">
              <div className="text-sm text-gray-500 mb-1">Total Queries</div>
              <div className="text-2xl font-bold">
                {metrics.total_queries.toLocaleString()}
              </div>
            </div>

            <div className="card">
              <div className="text-sm text-gray-500 mb-1">Avg Confidence Score</div>
              <div className="text-2xl font-bold">
                {(metrics.avg_confidence_score * 100).toFixed(1)}%
              </div>
              <div className="mt-2 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full"
                  style={{ width: `${metrics.avg_confidence_score * 100}%` }}
                />
              </div>
            </div>

            <div className="card">
              <div className="text-sm text-gray-500 mb-1">Avg Processing Time</div>
              <div className="text-2xl font-bold">
                {metrics.avg_processing_time_ms.toFixed(0)}ms
              </div>
            </div>
          </div>

          {/* Detailed Metrics */}
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Retrieval Metrics</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Avg Retrieved Chunks</span>
                  <span className="font-semibold">
                    {metrics.avg_retrieved_chunks.toFixed(1)}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Avg Citations</span>
                  <span className="font-semibold">
                    {metrics.avg_citations.toFixed(1)}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Avg Response Length</span>
                  <span className="font-semibold">
                    {metrics.avg_response_length.toFixed(0)} chars
                  </span>
                </div>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Query Distribution</h3>
              {metrics.query_type_distribution && (
                <div className="space-y-2">
                  {Object.entries(metrics.query_type_distribution).map(([type, count]) => (
                    <div key={type} className="flex justify-between items-center">
                      <span className="text-sm text-gray-600 capitalize">
                        {type.replace('_', ' ')}
                      </span>
                      <span className="font-semibold">{count as number}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Performance Chart */}
          <div className="card mb-8">
            <h3 className="text-lg font-semibold mb-4">Performance Overview</h3>
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h4 className="text-sm font-medium text-gray-600 mb-3">
                  Response Quality Metrics
                </h4>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart
                    data={[
                      {
                        name: 'Confidence',
                        value: metrics.avg_confidence_score * 100,
                      },
                      {
                        name: 'Citations',
                        value: (metrics.avg_citations / 10) * 100,
                      },
                      {
                        name: 'Chunks',
                        value: (metrics.avg_retrieved_chunks / 10) * 100,
                      },
                    ]}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Bar dataKey="value" fill="#0ea5e9" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div>
                <h4 className="text-sm font-medium text-gray-600 mb-3">
                  Processing Efficiency
                </h4>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Response Time</span>
                      <span>{metrics.avg_processing_time_ms.toFixed(0)}ms</span>
                    </div>
                    <div className="bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-500 h-2 rounded-full"
                        style={{
                          width: `${Math.min((metrics.avg_processing_time_ms / 5000) * 100, 100)}%`,
                        }}
                      />
                    </div>
                  </div>

                  <div className="pt-4 border-t">
                    <div className="text-sm text-gray-600 mb-2">
                      System Health Indicators
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-sm">Response Quality</span>
                        <span
                          className={`px-2 py-1 rounded text-xs font-semibold ${
                            metrics.avg_confidence_score > 0.7
                              ? 'bg-green-100 text-green-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}
                        >
                          {metrics.avg_confidence_score > 0.7 ? 'Good' : 'Fair'}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm">Citation Coverage</span>
                        <span
                          className={`px-2 py-1 rounded text-xs font-semibold ${
                            metrics.avg_citations > 3
                              ? 'bg-green-100 text-green-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}
                        >
                          {metrics.avg_citations > 3 ? 'Good' : 'Fair'}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-sm">Performance</span>
                        <span
                          className={`px-2 py-1 rounded text-xs font-semibold ${
                            metrics.avg_processing_time_ms < 3000
                              ? 'bg-green-100 text-green-800'
                              : 'bg-yellow-100 text-yellow-800'
                          }`}
                        >
                          {metrics.avg_processing_time_ms < 3000 ? 'Good' : 'Fair'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Evaluation Metrics Info */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h3 className="font-semibold text-blue-900 mb-3">
              📊 About These Metrics
            </h3>
            <div className="grid md:grid-cols-2 gap-4 text-sm text-blue-800">
              <div>
                <p className="font-medium mb-1">Confidence Score:</p>
                <p>
                  Measures the system's confidence in the accuracy of retrieved
                  information and generated responses.
                </p>
              </div>
              <div>
                <p className="font-medium mb-1">Processing Time:</p>
                <p>
                  End-to-end latency including retrieval, embedding generation,
                  and LLM response generation.
                </p>
              </div>
              <div>
                <p className="font-medium mb-1">Retrieved Chunks:</p>
                <p>
                  Number of relevant document chunks retrieved from the vector
                  database for each query.
                </p>
              </div>
              <div>
                <p className="font-medium mb-1">Citations:</p>
                <p>
                  Average number of citations included in responses for
                  provenance tracking and verification.
                </p>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Refresh Button */}
      <div className="mt-6 text-center">
        <button onClick={loadData} className="btn-secondary">
          Refresh Metrics
        </button>
      </div>
    </div>
  );
};

export default AnalyticsPage;
