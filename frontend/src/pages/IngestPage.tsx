import React, { useState } from 'react';
import { ingestAPI } from '../services/api';
import { DocumentPlusIcon, CloudArrowUpIcon } from '@heroicons/react/24/outline';

const IngestPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'text' | 'pdf'>('text');
  const [content, setContent] = useState('');
  const [title, setTitle] = useState('');
  const [sourceUrl, setSourceUrl] = useState('');
  const [documentType, setDocumentType] = useState('article');
  const [entityType, setEntityType] = useState('');
  const [entityId, setEntityId] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleTextIngest = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const metadata: any = {
        title,
        url: sourceUrl || undefined,
      };

      if (entityType && entityId) {
        metadata[`${entityType}_id`] = entityId;
      }

      const response = await ingestAPI.ingestDocument({
        content,
        metadata,
        document_type: documentType,
        source_url: sourceUrl || undefined,
      });

      setResult(response);
      // Reset form
      setContent('');
      setTitle('');
      setSourceUrl('');
      setEntityId('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred during ingestion');
    } finally {
      setLoading(false);
    }
  };

  const handlePDFIngest = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const metadata: any = {
        title: title || file.name,
      };

      if (entityType && entityId) {
        metadata[`${entityType}_id`] = entityId;
      }

      const response = await ingestAPI.ingestPDF(file, metadata);
      setResult(response);
      // Reset form
      setFile(null);
      setTitle('');
      setEntityId('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred during PDF ingestion');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Ingest Documents
        </h1>
        <p className="text-gray-600">
          Add startup news, funding announcements, investor theses, and market reports to the knowledge base
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-2 mb-6">
        <button
          onClick={() => setActiveTab('text')}
          className={`px-6 py-3 rounded-lg font-medium transition-colors ${
            activeTab === 'text'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Text Input
        </button>
        <button
          onClick={() => setActiveTab('pdf')}
          className={`px-6 py-3 rounded-lg font-medium transition-colors ${
            activeTab === 'pdf'
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          PDF Upload
        </button>
      </div>

      {/* Success Message */}
      {result && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
          <h3 className="font-semibold text-green-800 mb-2">
            ✓ Document Ingested Successfully
          </h3>
          <div className="text-sm text-green-700">
            <p>Document ID: {result.document_id}</p>
            <p>Chunks Created: {result.chunks_created}</p>
            <p>Status: {result.status}</p>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Text Input Form */}
      {activeTab === 'text' && (
        <form onSubmit={handleTextIngest} className="card">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Document Title *
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g., Series B Funding Announcement - TechCorp"
                className="input-field"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Document Type
              </label>
              <select
                value={documentType}
                onChange={(e) => setDocumentType(e.target.value)}
                className="input-field"
              >
                <option value="article">News Article</option>
                <option value="report">Research Report</option>
                <option value="announcement">Funding Announcement</option>
                <option value="thesis">Investment Thesis</option>
                <option value="policy">Policy Document</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Source URL (optional)
              </label>
              <input
                type="url"
                value={sourceUrl}
                onChange={(e) => setSourceUrl(e.target.value)}
                placeholder="https://example.com/article"
                className="input-field"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Entity Type (optional)
                </label>
                <select
                  value={entityType}
                  onChange={(e) => setEntityType(e.target.value)}
                  className="input-field"
                >
                  <option value="">None</option>
                  <option value="startup">Startup</option>
                  <option value="investor">Investor</option>
                  <option value="round">Funding Round</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Entity ID (optional)
                </label>
                <input
                  type="text"
                  value={entityId}
                  onChange={(e) => setEntityId(e.target.value)}
                  placeholder="e.g., startup_123"
                  className="input-field"
                  disabled={!entityType}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Content *
              </label>
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Paste the full document content here..."
                rows={12}
                className="input-field font-mono text-sm"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading || !content.trim() || !title.trim()}
              className="btn-primary w-full flex items-center justify-center space-x-2"
            >
              <DocumentPlusIcon className="h-5 w-5" />
              <span>{loading ? 'Ingesting...' : 'Ingest Document'}</span>
            </button>
          </div>
        </form>
      )}

      {/* PDF Upload Form */}
      {activeTab === 'pdf' && (
        <form onSubmit={handlePDFIngest} className="card">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Document Title (optional)
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Leave empty to use filename"
                className="input-field"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Entity Type (optional)
                </label>
                <select
                  value={entityType}
                  onChange={(e) => setEntityType(e.target.value)}
                  className="input-field"
                >
                  <option value="">None</option>
                  <option value="startup">Startup</option>
                  <option value="investor">Investor</option>
                  <option value="round">Funding Round</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Entity ID (optional)
                </label>
                <input
                  type="text"
                  value={entityId}
                  onChange={(e) => setEntityId(e.target.value)}
                  placeholder="e.g., startup_123"
                  className="input-field"
                  disabled={!entityType}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                PDF File *
              </label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                {file ? (
                  <div>
                    <p className="text-sm font-medium text-gray-900 mb-2">
                      {file.name}
                    </p>
                    <p className="text-xs text-gray-500 mb-4">
                      {(file.size / 1024).toFixed(2)} KB
                    </p>
                    <button
                      type="button"
                      onClick={() => setFile(null)}
                      className="btn-secondary text-sm"
                    >
                      Remove File
                    </button>
                  </div>
                ) : (
                  <div>
                    <CloudArrowUpIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <label className="btn-primary cursor-pointer">
                      Choose PDF File
                      <input
                        type="file"
                        accept=".pdf"
                        onChange={(e) => setFile(e.target.files?.[0] || null)}
                        className="hidden"
                      />
                    </label>
                    <p className="text-xs text-gray-500 mt-2">
                      Maximum file size: 10MB
                    </p>
                  </div>
                )}
              </div>
            </div>

            <button
              type="submit"
              disabled={loading || !file}
              className="btn-primary w-full flex items-center justify-center space-x-2"
            >
              <CloudArrowUpIcon className="h-5 w-5" />
              <span>{loading ? 'Uploading...' : 'Upload & Ingest PDF'}</span>
            </button>
          </div>
        </form>
      )}

      {/* Information Box */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">
          📝 Document Ingestion Guidelines
        </h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Documents are automatically chunked and embedded</li>
          <li>• Each chunk is stored with full provenance for citation tracking</li>
          <li>• Entity IDs help link documents to specific startups/investors</li>
          <li>• PDFs are automatically extracted and processed</li>
          <li>• All ingested content is searchable within seconds</li>
        </ul>
      </div>
    </div>
  );
};

export default IngestPage;
