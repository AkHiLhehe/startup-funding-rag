import React from 'react';
import { Link } from 'react-router-dom';
import { 
  MagnifyingGlassIcon, 
  DocumentPlusIcon, 
  ChartBarIcon,
  SparklesIcon,
  ShieldCheckIcon,
  BoltIcon 
} from '@heroicons/react/24/outline';

const HomePage: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center py-16">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          AI-Powered Investment Intelligence
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Turn fragmented startup and funding data into actionable intelligence. 
          Find the right investors for your startup or spot your next portfolio winner 
          with hyper-accurate, citation-backed insights.
        </p>
        <div className="flex justify-center space-x-4">
          <Link to="/search" className="btn-primary text-lg px-8 py-3">
            Start Searching
          </Link>
          <Link to="/ingest" className="btn-secondary text-lg px-8 py-3">
            Ingest Documents
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="grid md:grid-cols-3 gap-8 py-16">
        <div className="card text-center">
          <div className="flex justify-center mb-4">
            <SparklesIcon className="h-12 w-12 text-primary-600" />
          </div>
          <h3 className="text-xl font-semibold mb-2">RAG-Powered Search</h3>
          <p className="text-gray-600">
            Advanced retrieval-augmented generation using Gemini LLM and 
            Voyage AI embeddings for accurate, context-aware responses.
          </p>
        </div>

        <div className="card text-center">
          <div className="flex justify-center mb-4">
            <ShieldCheckIcon className="h-12 w-12 text-primary-600" />
          </div>
          <h3 className="text-xl font-semibold mb-2">Strict Citation Tracking</h3>
          <p className="text-gray-600">
            Every claim is backed by clear citations and provenance tracking 
            to eliminate hallucinations and ensure factual accuracy.
          </p>
        </div>

        <div className="card text-center">
          <div className="flex justify-center mb-4">
            <BoltIcon className="h-12 w-12 text-primary-600" />
          </div>
          <h3 className="text-xl font-semibold mb-2">Production-Grade</h3>
          <p className="text-gray-600">
            Built with FastAPI, Weaviate, and MongoDB for scalability, 
            with comprehensive evaluation metrics and monitoring.
          </p>
        </div>
      </div>

      {/* Use Cases Section */}
      <div className="py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Use Cases</h2>
        <div className="grid md:grid-cols-2 gap-8">
          <div className="card">
            <h3 className="text-xl font-semibold mb-3 text-primary-600">
              For Founders
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li>• Find investors matching your startup's stage and industry</li>
              <li>• Analyze investment theses and portfolio fit</li>
              <li>• Research funding trends and market signals</li>
              <li>• Prepare for investor meetings with comprehensive data</li>
            </ul>
          </div>

          <div className="card">
            <h3 className="text-xl font-semibold mb-3 text-primary-600">
              For VCs & Investors
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li>• Discover emerging startups in your focus areas</li>
              <li>• Analyze funding rounds and valuations</li>
              <li>• Track market trends and competitive intelligence</li>
              <li>• Due diligence research with verified sources</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Tech Stack Section */}
      <div className="py-16 bg-white rounded-lg shadow-md p-8">
        <h2 className="text-3xl font-bold text-center mb-8">Powered By</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div>
            <div className="text-lg font-semibold text-gray-900">Gemini</div>
            <div className="text-sm text-gray-600">LLM</div>
          </div>
          <div>
            <div className="text-lg font-semibold text-gray-900">Voyage AI</div>
            <div className="text-sm text-gray-600">Embeddings</div>
          </div>
          <div>
            <div className="text-lg font-semibold text-gray-900">Weaviate</div>
            <div className="text-sm text-gray-600">Vector DB</div>
          </div>
          <div>
            <div className="text-lg font-semibold text-gray-900">MongoDB</div>
            <div className="text-sm text-gray-600">Database</div>
          </div>
          <div>
            <div className="text-lg font-semibold text-gray-900">Tavily</div>
            <div className="text-sm text-gray-600">Web Search</div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="py-16">
        <h2 className="text-3xl font-bold text-center mb-8">Quick Actions</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <Link to="/search" className="card hover:shadow-lg transition-shadow cursor-pointer">
            <MagnifyingGlassIcon className="h-10 w-10 text-primary-600 mb-3" />
            <h3 className="text-lg font-semibold mb-2">Search Intelligence</h3>
            <p className="text-gray-600 text-sm">
              Ask questions about startups, investors, and funding trends
            </p>
          </Link>

          <Link to="/ingest" className="card hover:shadow-lg transition-shadow cursor-pointer">
            <DocumentPlusIcon className="h-10 w-10 text-primary-600 mb-3" />
            <h3 className="text-lg font-semibold mb-2">Ingest Documents</h3>
            <p className="text-gray-600 text-sm">
              Upload funding announcements, reports, and market data
            </p>
          </Link>

          <Link to="/analytics" className="card hover:shadow-lg transition-shadow cursor-pointer">
            <ChartBarIcon className="h-10 w-10 text-primary-600 mb-3" />
            <h3 className="text-lg font-semibold mb-2">View Analytics</h3>
            <p className="text-gray-600 text-sm">
              Track system performance and evaluation metrics
            </p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
