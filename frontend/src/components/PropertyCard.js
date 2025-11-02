import React from 'react';

const PropertyCard = ({ property, title }) => {
  if (!property) return null;

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

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      {/* Property Image */}
      {property.image_url && (
        <div className="h-48 overflow-hidden">
          <img 
            src={property.image_url} 
            alt={property.title || property.address}
            className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        </div>
      )}
      
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4">
        <h3 className="text-xl font-bold">{property.title || title}</h3>
        <p className="text-blue-100 break-words">{property.address}</p>
      </div>
      
      <div className="p-6">
        {/* Price */}
        <div className="text-center mb-6">
          <div className="text-3xl font-bold text-green-600">
            {formatPrice(property.market_value || property.display_price || property.predicted_price || 0)}
          </div>
          <div className="text-sm text-gray-500">
            {property.market_value ? 'Market Value' : 'Estimated Value'}
          </div>
          
          {/* Predicted Price Section */}
          {property.predicted_price && (
            <div className="mt-3 p-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
              <div className="text-lg font-bold text-blue-700">
                🤖 AI Predicted Price
              </div>
              <div className="text-2xl font-bold text-purple-600">
                {formatPrice(property.predicted_price)}
              </div>
              <div className="text-xs text-gray-600 mt-1">
                Based on ML analysis of property features
              </div>
              {property.market_value && property.predicted_price !== property.market_value && (
                <div className="text-sm mt-2">
                  <span className={`font-medium ${
                    property.predicted_price > property.market_value ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {property.predicted_price > property.market_value ? '📈 +' : '📉 -'}
                    {formatPrice(Math.abs(property.predicted_price - property.market_value))}
                  </span>
                  <span className="text-gray-500 text-xs ml-1">vs market value</span>
                </div>
              )}
            </div>
          )}
          
          {property.last_sold_price && (
            <div className="text-sm text-gray-600 mt-1">
              Last Sold: {formatPrice(property.last_sold_price)}
              {property.last_sold_date && (
                <span className="text-xs text-gray-500 block">
                  on {new Date(property.last_sold_date).toLocaleDateString()}
                </span>
              )}
            </div>
          )}
        </div>

        {/* Property Details */}
        <div className="space-y-3">
          <div className="flex justify-between items-center py-2 border-b border-gray-200">
            <span className="text-gray-600">Property Type</span>
            <span className="font-medium">{getPropertyTypeLabel(property.property_type)}</span>
          </div>
          
          {/* Show area based on property type - matches ML model schema */}
          {property.property_type === "SFH" && property.lot_area > 0 && (
            <div className="flex justify-between items-center py-2 border-b border-gray-200">
              <span className="text-gray-600">Lot Area</span>
              <span className="font-medium">{property.lot_area?.toLocaleString()} sq ft</span>
            </div>
          )}
          
          {property.property_type === "Condo" && property.building_area > 0 && (
            <div className="flex justify-between items-center py-2 border-b border-gray-200">
              <span className="text-gray-600">Building Area</span>
              <span className="font-medium">{property.building_area?.toLocaleString()} sq ft</span>
            </div>
          )}
          
          <div className="flex justify-between items-center py-2 border-b border-gray-200">
            <span className="text-gray-600">Bedrooms</span>
            <span className="font-medium">{property.bedrooms}</span>
          </div>
          
          <div className="flex justify-between items-center py-2 border-b border-gray-200">
            <span className="text-gray-600">Bathrooms</span>
            <span className="font-medium">{property.bathrooms}</span>
          </div>
          
          <div className="flex justify-between items-center py-2 border-b border-gray-200">
            <span className="text-gray-600">Year Built</span>
            <span className="font-medium">{property.year_built}</span>
          </div>
          
          <div className="flex justify-between items-center py-2 border-b border-gray-200">
            <span className="text-gray-600">School Rating</span>
            <span className="font-medium">{property.school_rating}/10</span>
          </div>
        </div>

        {/* Features */}
        <div className="mt-4">
          <h4 className="font-medium text-gray-700 mb-2">Features</h4>
          <div className="flex flex-wrap gap-2">
            {/* Show amenities from property data */}
            {property.amenities && property.amenities.length > 0 ? (
              property.amenities.slice(0, 6).map((amenity, index) => (
                <span key={index} className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                  {amenity.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </span>
              ))
            ) : (
              <>
                {property.has_pool && (
                  <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                    🏊‍♂️ Pool
                  </span>
                )}
                {property.has_garage && (
                  <span className="bg-gray-100 text-gray-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                    🚗 Garage
                  </span>
                )}
                {!property.has_pool && !property.has_garage && !property.amenities && (
                  <span className="text-gray-500 text-sm">No special features</span>
                )}
              </>
            )}
          </div>
          
          {/* Show additional details if available */}
          {property.square_footage && (
            <div className="mt-2 text-sm text-gray-600">
              <span className="font-medium">Size:</span> {property.square_footage.toLocaleString()} sq ft
            </div>
          )}
          
          {property.condition && (
            <div className="mt-1 text-sm text-gray-600">
              <span className="font-medium">Condition:</span> 
              <span className={`ml-1 capitalize ${
                property.condition === 'excellent' ? 'text-green-600' :
                property.condition === 'good' ? 'text-blue-600' :
                property.condition === 'fair' ? 'text-yellow-600' : 'text-gray-600'
              }`}>
                {property.condition}
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PropertyCard;