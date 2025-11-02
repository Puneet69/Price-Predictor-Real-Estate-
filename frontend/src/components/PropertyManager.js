import React, { useState, useEffect, useCallback } from 'react';

const PropertyManager = () => {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({});
  const [showAddForm, setShowAddForm] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedComparison, setSelectedComparison] = useState([]);
  const [dataSource, setDataSource] = useState('unknown');
  
  // Form state for adding new property
  const [newProperty, setNewProperty] = useState({
    address: '',
    property_type: 'SFH',
    lot_size: '',
    square_footage: '',
    bedrooms: '',
    bathrooms: '',
    garage: '',
    year_built: '',
    market_value: '',
    amenities: '',
    neighborhood_features: '',
    condition: 'fair'
  });

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const loadProperties = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/properties`);
      if (response.ok) {
        const data = await response.json();
        setProperties(data.properties || []);
        setDataSource(data.source || 'unknown');
      }
    } catch (error) {
      console.error('Error loading properties:', error);
    }
    setLoading(false);
  }, [API_BASE]);

  const loadStats = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/properties/stats/summary`);
      if (response.ok) {
        const data = await response.json();
        setStats(data);
        if (data.source) {
          setDataSource(data.source);
        }
      }
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  }, [API_BASE]);

  // Load properties on component mount
  useEffect(() => {
    loadProperties();
    loadStats();
  }, [loadProperties, loadStats]);

  const handleAddProperty = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      // Convert string arrays to actual arrays
      const propertyData = {
        ...newProperty,
        lot_size: parseInt(newProperty.lot_size) || 0,
        square_footage: parseInt(newProperty.square_footage) || 0,
        bedrooms: parseInt(newProperty.bedrooms) || 0,
        bathrooms: parseInt(newProperty.bathrooms) || 0,
        garage: parseInt(newProperty.garage) || 0,
        year_built: parseInt(newProperty.year_built) || 2000,
        market_value: parseInt(newProperty.market_value) || 0,
        amenities: newProperty.amenities.split(',').map(a => a.trim()).filter(a => a),
        neighborhood_features: newProperty.neighborhood_features.split(',').map(f => f.trim()).filter(f => f)
      };

      const response = await fetch(`${API_BASE}/properties`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(propertyData),
      });

      if (response.ok) {
        // Reset form
        setNewProperty({
          address: '',
          property_type: 'SFH',
          lot_size: '',
          square_footage: '',
          bedrooms: '',
          bathrooms: '',
          garage: '',
          year_built: '',
          market_value: '',
          amenities: '',
          neighborhood_features: '',
          condition: 'fair'
        });
        setShowAddForm(false);
        await loadProperties();
        await loadStats();
        alert('Property added successfully!');
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
      }
    } catch (error) {
      console.error('Error adding property:', error);
      alert('Error adding property');
    }
    setLoading(false);
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadProperties();
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/properties/search?query=${encodeURIComponent(searchQuery)}`);
      if (response.ok) {
        const data = await response.json();
        setProperties(data.properties || []);
      }
    } catch (error) {
      console.error('Error searching properties:', error);
    }
    setLoading(false);
  };

  const handleCompareToggle = (property) => {
    if (selectedComparison.find(p => p._id === property._id)) {
      setSelectedComparison(selectedComparison.filter(p => p._id !== property._id));
    } else if (selectedComparison.length < 2) {
      setSelectedComparison([...selectedComparison, property]);
    } else {
      alert('You can only compare 2 properties at a time');
    }
  };

  const handleCompare = async () => {
    if (selectedComparison.length !== 2) {
      alert('Please select exactly 2 properties to compare');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/compare-properties-mongo`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          address1: selectedComparison[0].address,
          address2: selectedComparison[1].address
        }),
      });

      if (response.ok) {
        const comparison = await response.json();
        
        // Display comparison results
        const resultWindow = window.open('', '_blank', 'width=800,height=600');
        resultWindow.document.write(`
          <html>
            <head><title>Property Comparison Results</title></head>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
              <h1>Property Comparison Results</h1>
              
              <div style="display: flex; gap: 20px;">
                <div style="flex: 1; border: 1px solid #ccc; padding: 15px; border-radius: 8px;">
                  <h3>Property 1</h3>
                  <p><strong>Address:</strong> ${comparison.property1.address}</p>
                  <p><strong>Type:</strong> ${comparison.property1.property_type}</p>
                  <p><strong>Price:</strong> $${comparison.property1.predicted_price?.toLocaleString()}</p>
                  <p><strong>Bedrooms:</strong> ${comparison.property1.bedrooms}</p>
                  <p><strong>Bathrooms:</strong> ${comparison.property1.bathrooms}</p>
                  <p><strong>Year Built:</strong> ${comparison.property1.year_built}</p>
                </div>
                
                <div style="flex: 1; border: 1px solid #ccc; padding: 15px; border-radius: 8px;">
                  <h3>Property 2</h3>
                  <p><strong>Address:</strong> ${comparison.property2.address}</p>
                  <p><strong>Type:</strong> ${comparison.property2.property_type}</p>
                  <p><strong>Price:</strong> $${comparison.property2.predicted_price?.toLocaleString()}</p>
                  <p><strong>Bedrooms:</strong> ${comparison.property2.bedrooms}</p>
                  <p><strong>Bathrooms:</strong> ${comparison.property2.bathrooms}</p>
                  <p><strong>Year Built:</strong> ${comparison.property2.year_built}</p>
                </div>
              </div>
              
              <div style="margin-top: 20px; padding: 15px; background-color: #f0f0f0; border-radius: 8px;">
                <h3>Comparison Summary</h3>
                <p><strong>Price Difference:</strong> $${comparison.price_difference?.toLocaleString()}</p>
                <p><strong>Higher Priced:</strong> ${comparison.higher_priced}</p>
              </div>
              
              <button onclick="window.close()" style="margin-top: 20px; padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">Close</button>
            </body>
          </html>
        `);
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail}`);
      }
    } catch (error) {
      console.error('Error comparing properties:', error);
      alert('Error comparing properties');
    }
    setLoading(false);
    setSelectedComparison([]);
  };

  return (
    <div className="property-manager">
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-800">Property Database Manager</h2>
          <div className="text-sm text-gray-600">
            Data Source: <span className="font-semibold capitalize text-blue-600">
              {dataSource === 'mongodb' ? 'MongoDB Database' : 
               dataSource === 'json_files' ? 'JSON Files' : 'Loading...'}
            </span>
          </div>
        </div>
        
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="font-semibold text-blue-800">Total Properties</h3>
            <p className="text-2xl font-bold text-blue-600">{stats.total_properties || 0}</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <h3 className="font-semibold text-green-800">Average Value</h3>
            <p className="text-2xl font-bold text-green-600">
              ${stats.average_market_value?.toLocaleString() || '0'}
            </p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <h3 className="font-semibold text-purple-800">Property Types</h3>
            <div className="text-sm text-purple-600">
              {Object.entries(stats.property_types || {}).map(([type, count]) => (
                <div key={type}>{type}: {count}</div>
              ))}
            </div>
          </div>
        </div>

        {/* Controls */}
        <div className="flex flex-wrap gap-4 mb-6">
          {dataSource === 'mongodb' && (
            <button
              onClick={() => setShowAddForm(!showAddForm)}
              className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
            >
              {showAddForm ? 'Cancel' : 'Add Property'}
            </button>
          )}
          
          {dataSource === 'json_files' && (
            <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-2 rounded-lg text-sm">
              <span className="font-semibold">📁 JSON Mode:</span> Viewing properties from JSON files. 
              To add properties, set up MongoDB.
            </div>
          )}
          
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Search properties..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="border border-gray-300 px-3 py-2 rounded-lg"
            />
            <button
              onClick={handleSearch}
              className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600"
            >
              Search
            </button>
          </div>

          {selectedComparison.length > 0 && (
            <div className="flex gap-2 items-center">
              <span className="text-gray-600">
                Selected: {selectedComparison.length}/2
              </span>
              <button
                onClick={handleCompare}
                disabled={selectedComparison.length !== 2}
                className="bg-orange-500 text-white px-4 py-2 rounded-lg hover:bg-orange-600 disabled:bg-gray-400"
              >
                Compare Properties
              </button>
              <button
                onClick={() => setSelectedComparison([])}
                className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
              >
                Clear Selection
              </button>
            </div>
          )}
        </div>

        {/* Add Property Form */}
        {showAddForm && (
          <form onSubmit={handleAddProperty} className="bg-gray-50 p-6 rounded-lg mb-6">
            <h3 className="text-lg font-semibold mb-4">Add New Property</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Address *</label>
                <input
                  type="text"
                  required
                  value={newProperty.address}
                  onChange={(e) => setNewProperty({...newProperty, address: e.target.value})}
                  className="w-full border border-gray-300 px-3 py-2 rounded-lg"
                  placeholder="123 Main St, City, State 12345"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Property Type *</label>
                <select
                  value={newProperty.property_type}
                  onChange={(e) => setNewProperty({...newProperty, property_type: e.target.value})}
                  className="w-full border border-gray-300 px-3 py-2 rounded-lg"
                >
                  <option value="SFH">Single Family Home</option>
                  <option value="Condo">Condo</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Lot Size (sq ft)</label>
                <input
                  type="number"
                  value={newProperty.lot_size}
                  onChange={(e) => setNewProperty({...newProperty, lot_size: e.target.value})}
                  className="w-full border border-gray-300 px-3 py-2 rounded-lg"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Square Footage</label>
                <input
                  type="number"
                  value={newProperty.square_footage}
                  onChange={(e) => setNewProperty({...newProperty, square_footage: e.target.value})}
                  className="w-full border border-gray-300 px-3 py-2 rounded-lg"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Bedrooms</label>
                <input
                  type="number"
                  value={newProperty.bedrooms}
                  onChange={(e) => setNewProperty({...newProperty, bedrooms: e.target.value})}
                  className="w-full border border-gray-300 px-3 py-2 rounded-lg"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Bathrooms</label>
                <input
                  type="number"
                  step="0.5"
                  value={newProperty.bathrooms}
                  onChange={(e) => setNewProperty({...newProperty, bathrooms: e.target.value})}
                  className="w-full border border-gray-300 px-3 py-2 rounded-lg"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Garage Spaces</label>
                <input
                  type="number"
                  value={newProperty.garage}
                  onChange={(e) => setNewProperty({...newProperty, garage: e.target.value})}
                  className="w-full border border-gray-300 px-3 py-2 rounded-lg"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Year Built</label>
                <input
                  type="number"
                  value={newProperty.year_built}
                  onChange={(e) => setNewProperty({...newProperty, year_built: e.target.value})}
                  className="w-full border border-gray-300 px-3 py-2 rounded-lg"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Market Value ($)</label>
                <input
                  type="number"
                  value={newProperty.market_value}
                  onChange={(e) => setNewProperty({...newProperty, market_value: e.target.value})}
                  className="w-full border border-gray-300 px-3 py-2 rounded-lg"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-1">Condition</label>
                <select
                  value={newProperty.condition}
                  onChange={(e) => setNewProperty({...newProperty, condition: e.target.value})}
                  className="w-full border border-gray-300 px-3 py-2 rounded-lg"
                >
                  <option value="excellent">Excellent</option>
                  <option value="good">Good</option>
                  <option value="fair">Fair</option>
                  <option value="poor">Poor</option>
                </select>
              </div>
              
              <div className="md:col-span-2">
                <label className="block text-sm font-medium mb-1">Amenities (comma-separated)</label>
                <input
                  type="text"
                  value={newProperty.amenities}
                  onChange={(e) => setNewProperty({...newProperty, amenities: e.target.value})}
                  className="w-full border border-gray-300 px-3 py-2 rounded-lg"
                  placeholder="pool, fireplace, deck, updated_kitchen"
                />
              </div>
              
              <div className="md:col-span-2">
                <label className="block text-sm font-medium mb-1">Neighborhood Features (comma-separated)</label>
                <input
                  type="text"
                  value={newProperty.neighborhood_features}
                  onChange={(e) => setNewProperty({...newProperty, neighborhood_features: e.target.value})}
                  className="w-full border border-gray-300 px-3 py-2 rounded-lg"
                  placeholder="good_schools, near_park, shopping_center"
                />
              </div>
            </div>
            
            <div className="mt-6 flex gap-4">
              <button
                type="submit"
                disabled={loading}
                className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-400"
              >
                {loading ? 'Adding...' : 'Add Property'}
              </button>
              <button
                type="button"
                onClick={() => setShowAddForm(false)}
                className="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600"
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        {/* Properties List */}
        <div className="property-list">
          <h3 className="text-lg font-semibold mb-4">
            Properties ({properties.length})
          </h3>
          
          {loading && (
            <div className="text-center py-8">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
              <p className="mt-2 text-gray-600">Loading...</p>
            </div>
          )}
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {properties.map((property) => (
              <div
                key={property._id}
                className={`bg-white border rounded-lg p-4 hover:shadow-md transition-shadow ${
                  selectedComparison.find(p => p._id === property._id) ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
                }`}
              >
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-semibold text-gray-800 text-sm leading-tight">
                    {property.address}
                  </h4>
                  <input
                    type="checkbox"
                    checked={!!selectedComparison.find(p => p._id === property._id)}
                    onChange={() => handleCompareToggle(property)}
                    className="ml-2"
                  />
                </div>
                
                <div className="text-sm text-gray-600 space-y-1">
                  <p><span className="font-medium">Type:</span> {property.property_type}</p>
                  <p><span className="font-medium">Bedrooms:</span> {property.bedrooms}</p>
                  <p><span className="font-medium">Bathrooms:</span> {property.bathrooms}</p>
                  <p><span className="font-medium">Year:</span> {property.year_built}</p>
                  {property.market_value > 0 && (
                    <p><span className="font-medium">Value:</span> ${property.market_value.toLocaleString()}</p>
                  )}
                  <p><span className="font-medium">Condition:</span> {property.condition}</p>
                </div>
                
                {property.amenities && property.amenities.length > 0 && (
                  <div className="mt-2">
                    <p className="text-xs text-gray-500">Amenities:</p>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {property.amenities.slice(0, 3).map((amenity, index) => (
                        <span
                          key={index}
                          className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs"
                        >
                          {amenity}
                        </span>
                      ))}
                      {property.amenities.length > 3 && (
                        <span className="text-gray-500 text-xs">+{property.amenities.length - 3} more</span>
                      )}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
          
          {!loading && properties.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No properties found. {searchQuery ? 'Try a different search.' : 'Add some properties to get started!'}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PropertyManager;