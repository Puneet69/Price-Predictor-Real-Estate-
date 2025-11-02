import React, { useState } from 'react';
import axios from 'axios';
import PropertyCard from './components/PropertyCard';
import LoadingSpinner from './components/LoadingSpinner';
import PropertyManager from './components/PropertyManager';
import PropertyBrowser from './components/PropertyBrowser';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('compare'); // 'compare' or 'manage'
  const [address1, setAddress1] = useState('');
  const [address2, setAddress2] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');


  const handleCompare = async (e) => {
    e.preventDefault();
    
    if (!address1.trim() || !address2.trim()) {
      setError('Please enter both property addresses');
      return;
    }

    setLoading(true);
    setError('');
    setResults(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/compare-properties`, {
        address1: address1.trim(),
        address2: address2.trim()
      });

      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to compare properties. Please try again.');
      console.error('Error comparing properties:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setAddress1('');
    setAddress2('');
    setResults(null);
    setError('');
  };



  const handlePropertySelect = (address, propertyNumber) => {
    if (propertyNumber === 1) {
      setAddress1(address);
    } else {
      setAddress2(address);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              🏠 Property Comparison & Management
            </h1>
            <p className="text-lg text-gray-600">
              Compare properties, manage your database, and get AI-powered insights
            </p>
          </div>

          {/* Tab Navigation */}
          <div className="flex justify-center mb-8">
            <div className="bg-white rounded-lg shadow-md p-1">
              <button
                onClick={() => setActiveTab('compare')}
                className={`px-6 py-2 rounded-md font-medium transition-all ${
                  activeTab === 'compare'
                    ? 'bg-blue-500 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Compare Properties
              </button>
              <button
                onClick={() => setActiveTab('manage')}
                className={`px-6 py-2 rounded-md font-medium transition-all ${
                  activeTab === 'manage'
                    ? 'bg-blue-500 text-white shadow-sm'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Manage Database
              </button>
            </div>
          </div>

          {/* Tab Content */}
          {activeTab === 'compare' && (
            <>
              {/* Property Browser */}
              <div className="mb-6">
                <PropertyBrowser 
                  onPropertySelect={handlePropertySelect}
                  selectedAddresses={[address1, address2]}
                />
              </div>

              {/* Input Form */}
              <div className="bg-white rounded-lg shadow-md p-6 mb-8">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Compare Properties</h3>
                <form onSubmit={handleCompare} className="space-y-4">
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label htmlFor="address1" className="block text-sm font-medium text-gray-700 mb-2">
                        Property Address 1
                      </label>
                      <input
                        type="text"
                        id="address1"
                        value={address1}
                        onChange={(e) => setAddress1(e.target.value)}
                        placeholder="Select from above or type address"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        disabled={loading}
                      />
                      {address1 && (
                        <p className="text-xs text-green-600 mt-1">✓ Property 1 selected</p>
                      )}
                    </div>
                    <div>
                      <label htmlFor="address2" className="block text-sm font-medium text-gray-700 mb-2">
                        Property Address 2
                      </label>
                      <input
                        type="text"
                        id="address2"
                        value={address2}
                        onChange={(e) => setAddress2(e.target.value)}
                        placeholder="Select from above or type address"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        disabled={loading}
                      />
                      {address2 && (
                        <p className="text-xs text-green-600 mt-1">✓ Property 2 selected</p>
                      )}
                    </div>
                  </div>

                  <div className="flex gap-4 justify-center">
                    <button
                      type="submit"
                      disabled={loading}
                      className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-2 px-6 rounded-md transition duration-200"
                    >
                      {loading ? 'Comparing...' : 'Compare Properties'}
                    </button>
                    
                    {results && (
                      <button
                        type="button"
                        onClick={resetForm}
                        className="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-6 rounded-md transition duration-200"
                      >
                        Reset
                      </button>
                    )}
                  </div>
                </form>

                {error && (
                  <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-md">
                    {error}
                  </div>
                )}
              </div>

              {/* Loading Spinner */}
              {loading && <LoadingSpinner />}

              {/* Results */}
              {results && !loading && (
                <div className="space-y-6">
                  {/* Summary */}
                  <div className="bg-white rounded-lg shadow-md p-6">
                    <h2 className="text-2xl font-bold text-gray-900 mb-4">📊 Comparison Summary</h2>
                    <div className="grid md:grid-cols-3 gap-4 text-center">
                      <div className="p-4 bg-blue-50 rounded-lg">
                        <h3 className="font-semibold text-gray-700">Price Difference</h3>
                        <p className="text-2xl font-bold text-blue-600">
                          ${results.price_difference?.toLocaleString() || '0'}
                        </p>
                        {results.percentage_difference && (
                          <p className="text-sm text-gray-600 mt-1">
                            {results.percentage_difference}% difference
                          </p>
                        )}
                      </div>
                      <div className="p-4 bg-green-50 rounded-lg">
                        <h3 className="font-semibold text-gray-700">Higher Priced</h3>
                        <p className="text-lg font-medium text-green-600 break-words">
                          {results.higher_priced ? 
                            (results.higher_priced.length > 30 ? 
                              results.higher_priced.substring(0, 30) + '...' : 
                              results.higher_priced) : 
                            'N/A'}
                        </p>
                        <p className="text-xs text-gray-500">
                          ${(results.property1?.address === results.higher_priced ? 
                              (results.property1?.market_value || results.property1?.display_price || 0) :
                              (results.property2?.market_value || results.property2?.display_price || 0)
                            ).toLocaleString()}
                        </p>
                      </div>
                      <div className="p-4 bg-orange-50 rounded-lg">
                        <h3 className="font-semibold text-gray-700">Lower Priced</h3>
                        <p className="text-lg font-medium text-orange-600 break-words">
                          {results.comparison_summary?.lower_property ? 
                            (results.comparison_summary.lower_property.length > 30 ? 
                              results.comparison_summary.lower_property.substring(0, 30) + '...' : 
                              results.comparison_summary.lower_property) : 
                            (results.higher_priced !== results.property1?.address ? 
                              (results.property1?.address?.length > 30 ? 
                                results.property1?.address.substring(0, 30) + '...' : 
                                results.property1?.address) : 
                              (results.property2?.address?.length > 30 ? 
                                results.property2?.address.substring(0, 30) + '...' : 
                                results.property2?.address))}
                        </p>
                        <p className="text-xs text-gray-500">
                          ${(results.property1?.address !== results.higher_priced ? 
                              (results.property1?.market_value || results.property1?.display_price || 0) :
                              (results.property2?.market_value || results.property2?.display_price || 0)
                            ).toLocaleString()}
                        </p>
                      </div>
                    </div>
                    
                    {/* Additional Comparison Details */}
                    {(results.property1 && results.property2) && (
                      <div className="mt-6 grid md:grid-cols-2 gap-4 text-sm">
                        <div className="bg-gray-50 p-3 rounded">
                          <h4 className="font-medium text-gray-700 mb-2">Property Details Comparison</h4>
                          <div className="space-y-1">
                            <div>Bedrooms: {results.property1?.bedrooms || 0} vs {results.property2?.bedrooms || 0}</div>
                            <div>Bathrooms: {results.property1?.bathrooms || 0} vs {results.property2?.bathrooms || 0}</div>
                            <div>Type: {results.property1?.property_type || 'N/A'} vs {results.property2?.property_type || 'N/A'}</div>
                            <div>Year Built: {results.property1?.year_built || 'N/A'} vs {results.property2?.year_built || 'N/A'}</div>
                          </div>
                        </div>
                        <div className="bg-gray-50 p-3 rounded">
                          <h4 className="font-medium text-gray-700 mb-2">Investment Analysis</h4>
                          <div className="space-y-1">
                            {results.property1?.property_tax && results.property2?.property_tax && (
                              <div>Property Tax: ${results.property1.property_tax?.toLocaleString()} vs ${results.property2.property_tax?.toLocaleString()}</div>
                            )}
                            {results.property1?.hoa_fee !== undefined && results.property2?.hoa_fee !== undefined && (
                              <div>HOA Fee: ${results.property1.hoa_fee}/mo vs ${results.property2.hoa_fee}/mo</div>
                            )}
                            {results.property1?.last_sold_price && results.property2?.last_sold_price && (
                              <div>Last Sold: ${results.property1.last_sold_price?.toLocaleString()} vs ${results.property2.last_sold_price?.toLocaleString()}</div>
                            )}
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Comparison Chart */}
                  {results.chart && (
                    <div className="bg-white rounded-lg shadow-md p-6">
                      <h2 className="text-2xl font-bold text-gray-900 mb-4">📊 Visual Comparison Dashboard</h2>
                      <div className="text-center">
                        <img 
                          src={`data:image/png;base64,${results.chart}`} 
                          alt="Property Comparison Chart" 
                          className="max-w-full h-auto mx-auto rounded-lg shadow-sm"
                          style={{ maxHeight: '600px' }}
                        />
                      </div>
                      <p className="text-sm text-gray-600 text-center mt-4">
                        📈 Interactive comparison dashboard showing market values, features, costs, and investment scores
                      </p>
                    </div>
                  )}

                  {/* Property Cards */}
                  <div className="grid lg:grid-cols-2 gap-6">
                    <PropertyCard property={results.property1} title="Property 1" />
                    <PropertyCard property={results.property2} title="Property 2" />
                  </div>
                </div>
              )}
            </>
          )}

          {/* Property Manager Tab */}
          {activeTab === 'manage' && (
            <PropertyManager />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;