"""
MongoDB Property Storage System
Handles storing and retrieving property data from MongoDB
"""

from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError, ConnectionFailure
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime
import re

class PropertyMongoStorage:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", database_name: str = "property_comparison"):
        """
        Initialize MongoDB connection
        
        Args:
            connection_string: MongoDB connection string
            database_name: Name of the database to use
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.db = None
        self.collection = None
        self.connect()
    
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.server_info()
            self.db = self.client[self.database_name]
            self.collection = self.db.properties
            
            # Create indexes for better performance
            self.create_indexes()
            print("✅ Connected to MongoDB successfully")
            
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            print("💡 Make sure MongoDB is running on your system")
            self.client = None
    
    def create_indexes(self):
        """Create database indexes for better query performance"""
        try:
            # Create text index for address search
            self.collection.create_index([("address", "text")])
            
            # Create compound index for property type and location
            self.collection.create_index([
                ("property_type", ASCENDING),
                ("city", ASCENDING),
                ("state", ASCENDING)
            ])
            
            # Create index for market value range queries
            self.collection.create_index([("market_value", ASCENDING)])
            
            print("✅ Database indexes created successfully")
            
        except Exception as e:
            print(f"⚠️ Error creating indexes: {e}")
    
    def is_connected(self) -> bool:
        """Check if MongoDB connection is active"""
        return self.client is not None
    
    def normalize_address(self, address: str) -> str:
        """Normalize address for consistent storage"""
        return re.sub(r'\s+', ' ', address.strip().lower())
    
    def parse_address(self, address: str) -> Dict[str, str]:
        """Parse address into components"""
        normalized = address.strip()
        parts = normalized.split(',')
        
        result = {
            "full_address": normalized,
            "street": "",
            "city": "",
            "state": "",
            "zip_code": ""
        }
        
        if len(parts) >= 1:
            result["street"] = parts[0].strip()
        if len(parts) >= 2:
            result["city"] = parts[1].strip()
        if len(parts) >= 3:
            # Try to extract state and zip from last part
            last_part = parts[2].strip()
            state_zip = last_part.split()
            if len(state_zip) >= 1:
                result["state"] = state_zip[0]
            if len(state_zip) >= 2:
                result["zip_code"] = state_zip[1]
        
        return result
    
    def add_property(self, property_data: Dict[str, Any]) -> bool:
        """
        Add a new property to the database
        
        Args:
            property_data: Dictionary containing property information
            
        Returns:
            bool: True if property was added successfully
        """
        if not self.is_connected():
            print("❌ Not connected to MongoDB")
            return False
        
        try:
            # Validate required fields
            required_fields = ['address', 'property_type']
            for field in required_fields:
                if field not in property_data:
                    print(f"❌ Missing required field: {field}")
                    return False
            
            # Parse and add address components
            address_info = self.parse_address(property_data['address'])
            property_data.update(address_info)
            
            # Add metadata
            property_data['created_at'] = datetime.utcnow()
            property_data['updated_at'] = datetime.utcnow()
            property_data['normalized_address'] = self.normalize_address(property_data['address'])
            
            # Set default values for missing fields
            defaults = {
                'lot_size': 0,
                'square_footage': 0,
                'bedrooms': 0,
                'bathrooms': 0,
                'garage': 0,
                'year_built': 2000,
                'market_value': 0,
                'amenities': [],
                'neighborhood_features': [],
                'condition': 'fair'
            }
            
            for key, default_value in defaults.items():
                if key not in property_data:
                    property_data[key] = default_value
            
            # Insert property
            result = self.collection.insert_one(property_data)
            
            if result.inserted_id:
                print(f"✅ Property added successfully: {property_data['address']}")
                print(f"   ID: {result.inserted_id}")
                return True
            else:
                print("❌ Failed to add property")
                return False
                
        except DuplicateKeyError:
            print(f"⚠️ Property already exists: {property_data.get('address', 'Unknown')}")
            return False
        except Exception as e:
            print(f"❌ Error adding property: {e}")
            return False
    
    def get_property_by_address(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Get property by address
        
        Args:
            address: Property address to search for
            
        Returns:
            Property data or None if not found
        """
        if not self.is_connected():
            return None
        
        try:
            normalized = self.normalize_address(address)
            property_data = self.collection.find_one({"normalized_address": normalized})
            
            if property_data:
                # Convert ObjectId to string for JSON serialization
                property_data['_id'] = str(property_data['_id'])
                return property_data
            
            return None
            
        except Exception as e:
            print(f"❌ Error retrieving property: {e}")
            return None
    
    def search_properties(self, query: str = "", limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search properties by text query
        
        Args:
            query: Search query (address, city, etc.)
            limit: Maximum number of results
            
        Returns:
            List of matching properties
        """
        if not self.is_connected():
            return []
        
        try:
            if query:
                # Text search
                cursor = self.collection.find(
                    {"$text": {"$search": query}},
                    {"score": {"$meta": "textScore"}}
                ).sort([("score", {"$meta": "textScore"})]).limit(limit)
            else:
                # Get all properties
                cursor = self.collection.find().limit(limit)
            
            properties = []
            for prop in cursor:
                prop['_id'] = str(prop['_id'])
                properties.append(prop)
            
            return properties
            
        except Exception as e:
            print(f"❌ Error searching properties: {e}")
            return []
    
    def get_all_properties(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get all properties from database
        
        Args:
            limit: Maximum number of properties to return
            
        Returns:
            List of all properties
        """
        return self.search_properties("", limit)
    
    def update_property(self, address: str, updates: Dict[str, Any]) -> bool:
        """
        Update property data
        
        Args:
            address: Property address
            updates: Dictionary of fields to update
            
        Returns:
            bool: True if update was successful
        """
        if not self.is_connected():
            return False
        
        try:
            normalized = self.normalize_address(address)
            updates['updated_at'] = datetime.utcnow()
            
            result = self.collection.update_one(
                {"normalized_address": normalized},
                {"$set": updates}
            )
            
            if result.modified_count > 0:
                print(f"✅ Property updated: {address}")
                return True
            else:
                print(f"⚠️ No property found to update: {address}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating property: {e}")
            return False
    
    def delete_property(self, address: str) -> bool:
        """
        Delete property from database
        
        Args:
            address: Property address
            
        Returns:
            bool: True if deletion was successful
        """
        if not self.is_connected():
            return False
        
        try:
            normalized = self.normalize_address(address)
            result = self.collection.delete_one({"normalized_address": normalized})
            
            if result.deleted_count > 0:
                print(f"✅ Property deleted: {address}")
                return True
            else:
                print(f"⚠️ No property found to delete: {address}")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting property: {e}")
            return False
    
    def get_properties_by_type(self, property_type: str) -> List[Dict[str, Any]]:
        """Get properties by type (SFH, Condo, etc.)"""
        if not self.is_connected():
            return []
        
        try:
            cursor = self.collection.find({"property_type": property_type})
            properties = []
            for prop in cursor:
                prop['_id'] = str(prop['_id'])
                properties.append(prop)
            return properties
        except Exception as e:
            print(f"❌ Error getting properties by type: {e}")
            return []
    
    def get_properties_by_price_range(self, min_price: int, max_price: int) -> List[Dict[str, Any]]:
        """Get properties within price range"""
        if not self.is_connected():
            return []
        
        try:
            cursor = self.collection.find({
                "market_value": {"$gte": min_price, "$lte": max_price}
            })
            properties = []
            for prop in cursor:
                prop['_id'] = str(prop['_id'])
                properties.append(prop)
            return properties
        except Exception as e:
            print(f"❌ Error getting properties by price range: {e}")
            return []
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        if not self.is_connected():
            return {}
        
        try:
            total_properties = self.collection.count_documents({})
            
            # Get property type distribution
            pipeline = [
                {"$group": {"_id": "$property_type", "count": {"$sum": 1}}}
            ]
            type_distribution = list(self.collection.aggregate(pipeline))
            
            # Get average market value
            avg_pipeline = [
                {"$group": {"_id": None, "avg_value": {"$avg": "$market_value"}}}
            ]
            avg_result = list(self.collection.aggregate(avg_pipeline))
            avg_value = avg_result[0]['avg_value'] if avg_result else 0
            
            return {
                "total_properties": total_properties,
                "property_types": {item['_id']: item['count'] for item in type_distribution},
                "average_market_value": round(avg_value, 2) if avg_value else 0
            }
            
        except Exception as e:
            print(f"❌ Error getting database stats: {e}")
            return {}
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✅ MongoDB connection closed")

# Test function
def test_mongodb_storage():
    """Test the MongoDB storage system"""
    print("🧪 TESTING MONGODB STORAGE")
    print("=" * 40)
    
    storage = PropertyMongoStorage()
    
    if not storage.is_connected():
        print("❌ MongoDB not available - skipping tests")
        return
    
    # Test property data
    test_property = {
        "address": "789 Test Street, Test City, CA 90210",
        "property_type": "SFH",
        "lot_size": 8000,
        "square_footage": 2500,
        "bedrooms": 4,
        "bathrooms": 3,
        "garage": 2,
        "year_built": 2020,
        "market_value": 850000,
        "amenities": ["pool", "fireplace", "modern_kitchen"],
        "neighborhood_features": ["great_schools", "near_shopping"],
        "condition": "excellent"
    }
    
    # Test adding property
    print("\n1. Testing property addition...")
    success = storage.add_property(test_property)
    print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    
    # Test retrieving property
    print("\n2. Testing property retrieval...")
    retrieved = storage.get_property_by_address(test_property["address"])
    print(f"   Result: {'✅ Found' if retrieved else '❌ Not found'}")
    if retrieved:
        print(f"   Address: {retrieved.get('address')}")
        print(f"   Value: ${retrieved.get('market_value'):,}")
    
    # Test search
    print("\n3. Testing property search...")
    results = storage.search_properties("Test City")
    print(f"   Found {len(results)} properties")
    
    # Test stats
    print("\n4. Testing database stats...")
    stats = storage.get_database_stats()
    print(f"   Total properties: {stats.get('total_properties', 0)}")
    print(f"   Property types: {stats.get('property_types', {})}")
    
    storage.close_connection()
    print("\n✅ MongoDB storage test completed!")

if __name__ == "__main__":
    test_mongodb_storage()