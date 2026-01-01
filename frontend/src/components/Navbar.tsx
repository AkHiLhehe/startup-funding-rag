import React from 'react';
import { Link } from 'react-router-dom';
import { MagnifyingGlassIcon, ChartBarIcon, DocumentPlusIcon } from '@heroicons/react/24/outline';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <div className="text-2xl font-bold text-primary-600">
              🚀 Startup Intelligence
            </div>
          </Link>

          <div className="flex space-x-4">
            <Link
              to="/search"
              className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <MagnifyingGlassIcon className="h-5 w-5" />
              <span>Search</span>
            </Link>

            <Link
              to="/ingest"
              className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <DocumentPlusIcon className="h-5 w-5" />
              <span>Ingest</span>
            </Link>

            <Link
              to="/analytics"
              className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <ChartBarIcon className="h-5 w-5" />
              <span>Analytics</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
