import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PropertyBrowser = ({ onPropertySelect, selectedAddresses = [] }) => {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState('all');

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    loadProperties();
  }, []);

  const loadProperties = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/properties`);
      if (response.data && response.data.properties) {
        setProperties(response.data.properties);
      }
    } catch (error) {
      console.error('Error loading properties:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredProperties = properties.filter(property => {
    const matchesSearch = !searchQuery || 
      property.address?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      property.city?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      property.state?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      property.neighborhood?.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesType = filterType === 'all' || property.property_type === filterType;
    
    return matchesSearch && matchesType;
  });

  const formatPrice = (price) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(price);
  };

  const getPropertyTypeLabel = (type) => {
    const types = {
      'SFH': 'Single Family Home',
      'Condo': 'Condominium'
    };
    return types[type] || type;
  };

  const isSelected = (address) => {
    return selectedAddresses.includes(address);
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1, 2, 3, 4, 5, 6].map(i => (
              <div key={i} className="border rounded-lg p-4">
                <div className="h-32 bg-gray-200 rounded mb-3"></div>
                <div className="h-4 bg-gray-200 rounded mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-2/3"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4 md:mb-0">
          Browse Properties ({filteredProperties.length})
        </h3>
        
        <div className="flex flex-col md:flex-row gap-3">
          {/* Search */}
          <input
            type="text"
            placeholder="Search by location..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          
          {/* Filter */}
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Types</option>
            <option value="SFH">Single Family Homes</option>
            <option value="Condo">Condominiums</option>
          </select>
        </div>
      </div>

      {/* Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-md p-3 mb-4">
        <p className="text-blue-800 text-sm">
          <span className="font-semibold">💡 How to compare:</span> Click on any property cards below to select them for comparison, 
          or use the "Select" buttons to choose Property 1 and Property 2.
        </p>
      </div>

      {/* Properties Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProperties.map((property) => (
          <div
            key={property.id}
            className={`border rounded-lg overflow-hidden hover:shadow-lg transition-all duration-200 cursor-pointer ${
              isSelected(property.address) ? 'ring-2 ring-blue-500 bg-blue-50' : 'hover:border-gray-300'
            }`}
          >
            {/* Property Image */}
            {property.image_url && (
              <div className="h-48 overflow-hidden">
                <img
                  src={property.image_url}
                  alt={property.address}
                  className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    e.target.style.display = 'none';
                  }}
                />
              </div>
            )}

            <div className="p-4">
              {/* Property Details */}
              <div className="mb-3">
                <h4 className="font-semibold text-gray-800 text-sm mb-1 line-clamp-2">
                  {property.title || property.address}
                </h4>
                <p className="text-xs text-gray-600 mb-2">{property.address}</p>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-lg font-bold text-green-600">
                    {formatPrice(property.market_value || 0)}
                  </span>
                  <span className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                    {getPropertyTypeLabel(property.property_type)}
                  </span>
                </div>
              </div>

              {/* Property Features */}
              <div className="text-xs text-gray-600 mb-3">
                <div className="flex justify-between">
                  <span>{property.bedrooms} beds</span>
                  <span>{property.bathrooms} baths</span>
                  <span>{property.square_footage?.toLocaleString()} sq ft</span>
                </div>
              </div>

              {/* Amenities Preview */}
              {property.amenities && property.amenities.length > 0 && (
                <div className="mb-3">
                  <div className="flex flex-wrap gap-1">
                    {property.amenities.slice(0, 2).map((amenity, index) => (
                      <span
                        key={index}
                        className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded"
                      >
                        {amenity.replace(/_/g, ' ')}
                      </span>
                    ))}
                    {property.amenities.length > 2 && (
                      <span className="text-xs text-gray-500">
                        +{property.amenities.length - 2} more
                      </span>
                    )}
                  </div>
                </div>
              )}

              {/* Selection Buttons */}
              <div className="flex gap-2">
                <button
                  onClick={() => onPropertySelect(property.address, 1)}
                  className={`flex-1 text-xs py-2 px-3 rounded font-medium transition-colors ${
                    selectedAddresses[0] === property.address
                      ? 'bg-blue-600 text-white'
                      : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                  }`}
                >
                  {selectedAddresses[0] === property.address ? '✓ Property 1' : 'Select as Property 1'}
                </button>
                <button
                  onClick={() => onPropertySelect(property.address, 2)}
                  className={`flex-1 text-xs py-2 px-3 rounded font-medium transition-colors ${
                    selectedAddresses[1] === property.address
                      ? 'bg-green-600 text-white'
                      : 'bg-green-100 text-green-700 hover:bg-green-200'
                  }`}
                >
                  {selectedAddresses[1] === property.address ? '✓ Property 2' : 'Select as Property 2'}
                </button>
              </div>

              {/* Selection Status */}
              {isSelected(property.address) && (
                <div className="mt-2 text-center">
                  <span className="text-xs font-medium text-blue-600">
                    ✓ Selected for comparison
                  </span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* No Results */}
      {filteredProperties.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-400 text-4xl mb-4">🏠</div>
          <h3 className="text-lg font-medium text-gray-600 mb-2">No properties found</h3>
          <p className="text-gray-500">Try adjusting your search or filter criteria</p>
        </div>
      )}
    </div>
  );
};

export default PropertyBrowser;