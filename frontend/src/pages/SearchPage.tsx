import React, { useState } from 'react';
import { searchAPI, SearchResponse, Citation } from '../services/api';
import { MagnifyingGlassIcon, SparklesIcon } from '@heroicons/react/24/outline';
import ReactMarkdown from 'react-markdown';

const SearchPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [queryType, setQueryType] = useState<'general' | 'investor_search' | 'startup_search' | 'funding_analysis' | 'market_intelligence'>('general');
  const [responseLanguage, setResponseLanguage] = useState<string>('auto');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<SearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await searchAPI.search({
        query,
        query_type: queryType,
        top_k: 10,
        include_citations: true,
        response_language: responseLanguage === 'auto' ? undefined : responseLanguage,
      });
      setResult(response);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred while searching');
    } finally {
      setLoading(false);
    }
  };

  const exampleQueries = [
    "What are the recent funding trends in AI startups?",
    "Tell me about Sequoia Capital's investment thesis",
    "Which investors focus on early-stage fintech startups?",
    "What's the average Series A funding amount in 2024?",
  ];

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Investment Intelligence Search
        </h1>
        <p className="text-gray-600">
          Ask questions about startups, investors, funding rounds, and market trends
        </p>
      </div>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="card mb-8">
        <div className=\"grid grid-cols-1 md:grid-cols-2 gap-4 mb-4\">
          <div>
            <label className=\"block text-sm font-medium text-gray-700 mb-2\">
              Query Type
            </label>
            <select
              value={queryType}
              onChange={(e) => setQueryType(e.target.value as any)}
              className=\"input-field\"
            >
              <option value=\"general\">General</option>
              <option value=\"investor_search\">Investor Search</option>
              <option value=\"startup_search\">Startup Search</option>
              <option value=\"funding_analysis\">Funding Analysis</option>
              <option value=\"market_intelligence\">Market Intelligence</option>
            </select>
          </div>

          <div>
            <label className=\"block text-sm font-medium text-gray-700 mb-2\">
              Response Language 🌍
            </label>
            <select
              value={responseLanguage}
              onChange={(e) => setResponseLanguage(e.target.value)}
              className=\"input-field\"
            >
              <option value=\"auto\">Auto-detect</option>
              <option value=\"en\">English</option>
              <option value=\"hi\">हिंदी (Hindi)</option>
              <option value=\"ta\">தமிழ் (Tamil)</option>
              <option value=\"te\">తెలుగు (Telugu)</option>
              <option value=\"bn\">বাংলা (Bengali)</option>
              <option value=\"mr\">मराठी (Marathi)</option>
              <option value=\"gu\">ગુજરાતી (Gujarati)</option>
              <option value=\"kn\">ಕನ್ನಡ (Kannada)</option>
              <option value=\"ml\">മലയാളം (Malayalam)</option>
              <option value=\"pa\">ਪੰਜਾਬੀ (Punjabi)</option>
              <option value=\"ur\">اردو (Urdu)</option>
            </select>
          </div>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Your Question
          </label>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., Which investors focus on Series A fintech startups in SF?"
            rows={4}
            className="input-field"
          />
        </div>

        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="btn-primary w-full flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
              <SparklesIcon className="h-5 w-5 animate-spin" />
              <span>Searching...</span>
            </>
          ) : (
            <>
              <MagnifyingGlassIcon className="h-5 w-5" />
              <span>Search</span>
            </>
          )}
        </button>
      </form>

      {/* Example Queries */}
      {!result && !loading && (
        <div className="card mb-8">
          <h3 className="font-semibold mb-3">Example Queries:</h3>
          <div className="space-y-2">
            {exampleQueries.map((example, index) => (
              <button
                key={index}
                onClick={() => setQuery(example)}
                className="block w-full text-left px-4 py-2 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors text-sm"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Metadata */}
          <div className="card">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <div className="text-gray-500">Confidence</div>
                <div className="font-semibold text-lg">
                  {(result.confidence_score * 100).toFixed(0)}%
                </div>
              </div>
              <div>
                <div className="text-gray-500">Processing Time</div>
                <div className="font-semibold text-lg">
                  {result.processing_time.toFixed(2)}s
                </div>
              </div>
              <div>
                <div className="text-gray-500">Sources Retrieved</div>
                <div className="font-semibold text-lg">
                  {result.retrieved_chunks}
                </div>
              </div>
              <div>
                <div className="text-gray-500">Citations</div>
                <div className="font-semibold text-lg">
                  {result.citations.length}
                </div>
              </div>
            </div>
          </div>

          {/* Answer */}
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Answer</h2>
            <div className="prose max-w-none">
              <ReactMarkdown>{result.answer}</ReactMarkdown>
            </div>
          </div>

          {/* Citations */}
          {result.citations.length > 0 && (
            <div className="card">
              <h2 className="text-xl font-semibold mb-4">Citations & Sources</h2>
              <div className="space-y-4">
                {result.citations.map((citation, index) => (
                  <div
                    key={index}
                    className="border-l-4 border-primary-500 pl-4 py-2"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <span className="inline-block bg-primary-100 text-primary-800 text-xs font-semibold px-2 py-1 rounded">
                          [{index + 1}]
                        </span>
                        <span className="ml-2 font-semibold">
                          {citation.source_title}
                        </span>
                      </div>
                      <span className="text-sm text-gray-500">
                        {(citation.confidence_score * 100).toFixed(0)}% confidence
                      </span>
                    </div>
                    <p className="text-sm text-gray-700 mb-2">
                      {citation.excerpt}
                    </p>
                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                      <span className="px-2 py-1 bg-gray-100 rounded">
                        {citation.source_type}
                      </span>
                      {citation.source_url && (
                        <a
                          href={citation.source_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-primary-600 hover:underline"
                        >
                          View Source →
                        </a>
                      )}
                      {citation.published_date && (
                        <span>{new Date(citation.published_date).toLocaleDateString()}</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchPage;
