#!/usr/bin/env python3
"""
Import Properties to MongoDB
This script imports all property JSON files into MongoDB for the Property Comparison App
"""

import os
import json
import sys
from pathlib import Path

# Add the backend directory to the path to import mongodb_storage
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from mongodb_storage import PropertyMongoStorage
except ImportError as e:
    print(f"❌ Error importing MongoDB storage: {e}")
    print("💡 Make sure you're running this from the project root and have installed pymongo")
    sys.exit(1)

def load_json_file(file_path: str):
    """Load and return JSON data from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return None

def convert_to_mongo_format(property_data: dict):
    """Convert property data to MongoDB-compatible format"""
    # Map the JSON structure to MongoDB expected structure
    mongo_data = {
        "address": property_data.get("address", ""),
        "property_type": property_data.get("property_type", "SFH"),
        "lot_size": property_data.get("lot_area", 0),
        "square_footage": property_data.get("building_area", 0) or property_data.get("lot_area", 0),
        "bedrooms": property_data.get("bedrooms", 0),
        "bathrooms": property_data.get("bathrooms", 0),
        "garage": 1 if property_data.get("has_garage", False) else 0,
        "year_built": property_data.get("year_built", 2000),
        "market_value": property_data.get("market_value", 0),
        "amenities": [],
        "neighborhood_features": [],
        "condition": "good"  # Default condition
    }
    
    # Convert features to amenities
    features = property_data.get("features", [])
    amenities = []
    for feature in features:
        # Convert feature names to standardized amenity names
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
            # Keep original feature name, clean it up
            clean_feature = feature_lower.replace(" ", "_").replace("-", "_")
            amenities.append(clean_feature)
    
    mongo_data["amenities"] = amenities
    
    # Convert nearby amenities to neighborhood features
    nearby = property_data.get("nearby_amenities", [])
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
            # Keep original amenity name, clean it up
            clean_amenity = amenity.split(" - ")[0].lower().replace(" ", "_").replace("-", "_")
            neighborhood_features.append(clean_amenity)
    
    mongo_data["neighborhood_features"] = neighborhood_features
    
    # Add additional fields from JSON if available
    if "neighborhood" in property_data:
        mongo_data["neighborhood"] = property_data["neighborhood"]
    if "last_sold_price" in property_data:
        mongo_data["last_sold_price"] = property_data["last_sold_price"]
    if "last_sold_date" in property_data:
        mongo_data["last_sold_date"] = property_data["last_sold_date"]
    if "property_tax" in property_data:
        mongo_data["property_tax"] = property_data["property_tax"]
    if "hoa_fee" in property_data:
        mongo_data["hoa_fee"] = property_data["hoa_fee"]
    
    return mongo_data

def import_properties_to_mongodb():
    """Import all property JSON files to MongoDB"""
    print("🏠 PROPERTY DATA IMPORT TO MONGODB")
    print("=" * 50)
    
    # Initialize MongoDB storage
    try:
        storage = PropertyMongoStorage()
        if not storage.is_connected():
            print("❌ Could not connect to MongoDB")
            print("💡 Make sure MongoDB is running:")
            print("   - Local: brew services start mongodb/brew/mongodb-community")
            print("   - Docker: docker-compose up mongodb -d")
            return False
        
        print("✅ Connected to MongoDB successfully")
        
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        return False
    
    # Find all property JSON files
    properties_dir = Path("dataset/properties")
    if not properties_dir.exists():
        print(f"❌ Properties directory not found: {properties_dir}")
        return False
    
    json_files = list(properties_dir.glob("*.json"))
    if not json_files:
        print(f"❌ No JSON files found in {properties_dir}")
        return False
    
    print(f"📁 Found {len(json_files)} property files to import")
    
    # Import each property
    imported_count = 0
    skipped_count = 0
    error_count = 0
    
    for json_file in json_files:
        print(f"\n📄 Processing: {json_file.name}")
        
        # Load JSON data
        property_data = load_json_file(json_file)
        if not property_data:
            print(f"   ❌ Failed to load JSON data")
            error_count += 1
            continue
        
        # Convert to MongoDB format
        try:
            mongo_data = convert_to_mongo_format(property_data)
            print(f"   📍 Address: {mongo_data.get('address', 'Unknown')}")
            print(f"   🏠 Type: {mongo_data.get('property_type', 'Unknown')}")
            print(f"   💰 Value: ${mongo_data.get('market_value', 0):,}")
            
            # Check if property already exists
            existing = storage.get_property_by_address(mongo_data['address'])
            if existing:
                print(f"   ⚠️  Property already exists, skipping...")
                skipped_count += 1
                continue
            
            # Add to MongoDB
            success = storage.add_property(mongo_data)
            if success:
                print(f"   ✅ Successfully imported")
                imported_count += 1
            else:
                print(f"   ❌ Failed to import")
                error_count += 1
                
        except Exception as e:
            print(f"   ❌ Error processing property: {e}")
            error_count += 1
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 IMPORT SUMMARY")
    print(f"✅ Successfully imported: {imported_count}")
    print(f"⚠️  Skipped (already exists): {skipped_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📁 Total files processed: {len(json_files)}")
    
    # Show database stats
    if imported_count > 0:
        print("\n🔍 DATABASE STATS AFTER IMPORT:")
        stats = storage.get_database_stats()
        print(f"   Total properties: {stats.get('total_properties', 0)}")
        print(f"   Property types: {stats.get('property_types', {})}")
        print(f"   Average value: ${stats.get('average_market_value', 0):,.2f}")
        
        print("\n🏠 ALL PROPERTIES IN DATABASE:")
        properties = storage.get_all_properties()
        for i, prop in enumerate(properties, 1):
            print(f"   {i}. {prop.get('address', 'Unknown')} - ${prop.get('market_value', 0):,} ({prop.get('property_type', 'Unknown')})")
    
    # Close connection
    storage.close_connection()
    
    print(f"\n🎉 Import completed! {imported_count} new properties added to database.")
    print("🚀 You can now use the Property Manager to view and compare these properties!")
    
    return imported_count > 0

if __name__ == "__main__":
    # Change to the correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir.parent)
    
    success = import_properties_to_mongodb()
    if success:
        print("\n💡 Next steps:")
        print("   1. Start the backend server: cd backend && python main.py")
        print("   2. Start the frontend: cd frontend && npm start")
        print("   3. Go to http://localhost:3000 and click 'Manage Database' tab")
        print("   4. You'll see all imported properties available for comparison!")
    else:
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure MongoDB is running")
        print("   2. Install pymongo: pip install pymongo")
        print("   3. Check that JSON files exist in dataset/properties/")