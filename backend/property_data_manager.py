#!/usr/bin/env python3
"""
Property Data Manager - Load JSON properties into application
Works with or without MongoDB
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

class PropertyDataManager:
    def __init__(self, dataset_path: str = "dataset"):
        """Initialize the property data manager"""
        self.dataset_path = Path(dataset_path)
        self.properties_dir = self.dataset_path / "properties"
        self.properties = []
        self.load_all_properties()
    
    def load_all_properties(self):
        """Load all property JSON files"""
        print("🏠 Loading property data from JSON files...")
        
        if not self.properties_dir.exists():
            print(f"⚠️  Properties directory not found: {self.properties_dir}")
            return
        
        json_files = list(self.properties_dir.glob("*.json"))
        if not json_files:
            print(f"⚠️  No JSON files found in {self.properties_dir}")
            return
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    property_data = json.load(f)
                    
                # Convert to standardized format
                standardized = self.standardize_property_data(property_data)
                self.properties.append(standardized)
                
            except Exception as e:
                print(f"❌ Error loading {json_file}: {e}")
        
        print(f"✅ Loaded {len(self.properties)} properties from JSON files")
        for prop in self.properties:
            print(f"   📍 {prop.get('address', 'Unknown')} - ${prop.get('market_value', 0):,}")
    
    def standardize_property_data(self, data: dict) -> dict:
        """Convert property data to standardized format"""
        # Create standardized property data
        standardized = {
            "address": data.get("address", ""),
            "property_type": data.get("property_type", "SFH"),
            "lot_size": data.get("lot_area", 0),
            "square_footage": data.get("building_area", 0) or data.get("lot_area", 0),
            "bedrooms": data.get("bedrooms", 0),
            "bathrooms": data.get("bathrooms", 0),
            "garage": 1 if data.get("has_garage", False) else 0,
            "year_built": data.get("year_built", 2000),
            "market_value": data.get("market_value", 0),
            "condition": "good"
        }
        
        # Process amenities
        features = data.get("features", [])
        amenities = []
        for feature in features:
            feature_lower = feature.lower()
            if "pool" in feature_lower:
                amenities.append("pool")
            elif "garage" in feature_lower or "parking" in feature_lower:
                amenities.append("garage")
            elif "kitchen" in feature_lower:
                amenities.append("updated_kitchen")
            elif "hardwood" in feature_lower:
                amenities.append("hardwood_floors")
            elif "fireplace" in feature_lower:
                amenities.append("fireplace")
            elif "deck" in feature_lower or "balcony" in feature_lower:
                amenities.append("deck")
            else:
                clean_feature = feature.lower().replace(" ", "_").replace("-", "_")
                amenities.append(clean_feature)
        
        standardized["amenities"] = amenities
        
        # Process neighborhood features
        nearby = data.get("nearby_amenities", [])
        neighborhood_features = []
        for amenity in nearby:
            amenity_lower = amenity.lower()
            if "school" in amenity_lower:
                neighborhood_features.append("good_schools")
            elif "park" in amenity_lower:
                neighborhood_features.append("near_park")
            elif "shopping" in amenity_lower:
                neighborhood_features.append("shopping_center")
            elif "transportation" in amenity_lower or "metro" in amenity_lower:
                neighborhood_features.append("public_transport")
            else:
                clean_amenity = amenity.split(" - ")[0].lower().replace(" ", "_")
                neighborhood_features.append(clean_amenity)
        
        standardized["neighborhood_features"] = neighborhood_features
        
        # Add extra fields
        extra_fields = ["neighborhood", "last_sold_price", "last_sold_date", 
                       "property_tax", "hoa_fee", "city", "state", "zip_code"]
        for field in extra_fields:
            if field in data:
                standardized[field] = data[field]
        
        # Add property image URL from Pexels
        property_images = [
            "https://images.pexels.com/photos/106399/pexels-photo-106399.jpeg",
            "https://images.pexels.com/photos/259588/pexels-photo-259588.jpeg", 
            "https://images.pexels.com/photos/323780/pexels-photo-323780.jpeg",
            "https://images.pexels.com/photos/271624/pexels-photo-271624.jpeg",
            "https://images.pexels.com/photos/534151/pexels-photo-534151.jpeg",
            "https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg",
            "https://images.pexels.com/photos/1571460/pexels-photo-1571460.jpeg",
            "https://images.pexels.com/photos/1918291/pexels-photo-1918291.jpeg",
            "https://images.pexels.com/photos/2079246/pexels-photo-2079246.jpeg",
            "https://images.pexels.com/photos/2121121/pexels-photo-2121121.jpeg",
            "https://images.pexels.com/photos/2635038/pexels-photo-2635038.jpeg",
            "https://images.pexels.com/photos/3075998/pexels-photo-3075998.jpeg",
            "https://images.pexels.com/photos/3288103/pexels-photo-3288103.jpeg",
            "https://images.pexels.com/photos/4050290/pexels-photo-4050290.jpeg",
            "https://images.pexels.com/photos/4172933/pexels-photo-4172933.jpeg",
            "https://images.pexels.com/photos/5824904/pexels-photo-5824904.jpeg",
            "https://images.pexels.com/photos/6186078/pexels-photo-6186078.jpeg",
            "https://images.pexels.com/photos/6782351/pexels-photo-6782351.jpeg",
            "https://images.pexels.com/photos/7031728/pexels-photo-7031728.jpeg",
            "https://images.pexels.com/photos/7578945/pexels-photo-7578945.jpeg",
            "https://images.pexels.com/photos/8031905/pexels-photo-8031905.jpeg",
            "https://images.pexels.com/photos/8293778/pexels-photo-8293778.jpeg",
            "https://images.pexels.com/photos/9146734/pexels-photo-9146734.jpeg",
            "https://images.pexels.com/photos/10129666/pexels-photo-10129666.jpeg"
        ]
        
        # Cycle through images based on address hash
        address_hash = hash(data.get("address", "")) % len(property_images)
        standardized["image_url"] = property_images[address_hash]
        
        return standardized
    
    def get_all_properties(self) -> List[Dict[str, Any]]:
        """Get all loaded properties"""
        return self.properties.copy()
    
    def get_property_by_address(self, address: str) -> Optional[Dict[str, Any]]:
        """Get property by address"""
        address_lower = address.lower().strip()
        for prop in self.properties:
            if prop.get("address", "").lower().strip() == address_lower:
                return prop
        return None
    
    def search_properties(self, query: str) -> List[Dict[str, Any]]:
        """Search properties by text"""
        if not query:
            return self.get_all_properties()
        
        query_lower = query.lower()
        results = []
        
        for prop in self.properties:
            # Search in address, neighborhood, city, amenities
            searchable_text = " ".join([
                prop.get("address", ""),
                prop.get("neighborhood", ""),
                prop.get("city", ""),
                " ".join(prop.get("amenities", [])),
                " ".join(prop.get("neighborhood_features", []))
            ]).lower()
            
            if query_lower in searchable_text:
                results.append(prop)
        
        return results
    
    def get_properties_by_type(self, property_type: str) -> List[Dict[str, Any]]:
        """Get properties by type"""
        return [prop for prop in self.properties if prop.get("property_type") == property_type]
    
    def get_properties_by_price_range(self, min_price: int, max_price: int) -> List[Dict[str, Any]]:
        """Get properties within price range"""
        return [
            prop for prop in self.properties 
            if min_price <= prop.get("market_value", 0) <= max_price
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get property statistics"""
        if not self.properties:
            return {"total_properties": 0, "property_types": {}, "average_market_value": 0}
        
        total = len(self.properties)
        
        # Property type distribution
        type_counts = {}
        total_value = 0
        
        for prop in self.properties:
            prop_type = prop.get("property_type", "Unknown")
            type_counts[prop_type] = type_counts.get(prop_type, 0) + 1
            total_value += prop.get("market_value", 0)
        
        avg_value = total_value / total if total > 0 else 0
        
        return {
            "total_properties": total,
            "property_types": type_counts,
            "average_market_value": round(avg_value, 2)
        }

def test_property_manager():
    """Test the property data manager"""
    print("🧪 TESTING PROPERTY DATA MANAGER")
    print("=" * 40)
    
    # Initialize manager
    manager = PropertyDataManager()
    
    if not manager.properties:
        print("❌ No properties loaded")
        return
    
    # Test stats
    stats = manager.get_stats()
    print(f"\n📊 STATISTICS:")
    print(f"   Total properties: {stats['total_properties']}")
    print(f"   Property types: {stats['property_types']}")
    print(f"   Average value: ${stats['average_market_value']:,.2f}")
    
    # Test search
    print(f"\n🔍 SEARCH TEST (query: 'San Francisco'):")
    results = manager.search_properties("San Francisco")
    print(f"   Found {len(results)} properties")
    for prop in results:
        print(f"   - {prop.get('address', 'Unknown')}")
    
    # Test by type
    print(f"\n🏠 PROPERTIES BY TYPE:")
    for prop_type in stats['property_types']:
        props = manager.get_properties_by_type(prop_type)
        print(f"   {prop_type}: {len(props)} properties")
    
    print("\n✅ Property data manager test completed!")

if __name__ == "__main__":
    test_property_manager()