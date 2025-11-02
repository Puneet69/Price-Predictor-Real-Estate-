#!/usr/bin/env python3
"""
Property Data Converter - Convert and merge JSON 1, 2, 3.txt files
Creates comprehensive property data with images and default values
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

def load_json_txt_file(file_path: str) -> List[Dict]:
    """Load JSON data from .txt file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {e}")
        return []

def generate_default_property_data(property_id: int, base_data: Dict, details: Dict, image_data: Dict) -> Dict:
    """Generate comprehensive property data with defaults"""
    
    # Extract base information
    title = base_data.get('title', f'Property {property_id}')
    price = base_data.get('price', 500000)
    location = base_data.get('location', 'Unknown Location')
    
    # Parse location
    location_parts = location.split(', ')
    city = location_parts[0] if len(location_parts) > 0 else 'Unknown City'
    state_zip = location_parts[1] if len(location_parts) > 1 else 'XX'
    state = state_zip.split()[0] if state_zip else 'XX'
    
    # Create full address
    street_names = [
        "Main Street", "Oak Avenue", "Pine Road", "Elm Street", "Cedar Lane",
        "Maple Drive", "Park Avenue", "First Street", "Second Avenue", "Broadway"
    ]
    street_number = random.randint(100, 9999)
    street_name = random.choice(street_names)
    full_address = f"{street_number} {street_name}, {city}, {state}"
    
    # Extract details
    bedrooms = details.get('bedrooms', 2)
    bathrooms = details.get('bathrooms', 2)
    size_sqft = details.get('size_sqft', 1500)
    amenities = details.get('amenities', [])
    
    # Determine property type based on bedrooms and title
    if 'villa' in title.lower() or 'house' in title.lower() or 'townhouse' in title.lower() or bedrooms >= 4:
        property_type = 'SFH'
        lot_size = random.randint(3000, 10000)
        square_footage = size_sqft
    else:
        property_type = 'Condo'
        lot_size = 0
        square_footage = size_sqft
    
    # Generate year built (realistic range)
    year_built = random.randint(1980, 2023)
    
    # Generate realistic additional data
    last_sold_date = datetime.now() - timedelta(days=random.randint(30, 1095))
    last_sold_price = int(price * random.uniform(0.8, 0.95))
    property_tax = int(price * 0.012)  # ~1.2% property tax
    hoa_fee = random.randint(0, 800) if property_type == 'Condo' else 0
    
    # Convert amenities to standardized format
    standardized_amenities = []
    for amenity in amenities:
        amenity_lower = amenity.lower()
        if 'pool' in amenity_lower or 'swimming' in amenity_lower:
            standardized_amenities.append('pool')
        elif 'gym' in amenity_lower or 'fitness' in amenity_lower:
            standardized_amenities.append('fitness_center')
        elif 'garage' in amenity_lower or 'parking' in amenity_lower:
            standardized_amenities.append('garage')
        elif 'garden' in amenity_lower or 'backyard' in amenity_lower:
            standardized_amenities.append('garden')
        elif 'smart' in amenity_lower:
            standardized_amenities.append('smart_home')
        elif 'security' in amenity_lower:
            standardized_amenities.append('security_system')
        elif 'terrace' in amenity_lower or 'balcony' in amenity_lower:
            standardized_amenities.append('balcony')
        elif 'dock' in amenity_lower:
            standardized_amenities.append('private_dock')
        else:
            # Keep original but clean it up
            clean_amenity = amenity_lower.replace(' ', '_').replace('-', '_')
            standardized_amenities.append(clean_amenity)
    
    # Add some default amenities if none
    if not standardized_amenities:
        default_amenities = ['updated_kitchen', 'air_conditioning', 'hardwood_floors']
        standardized_amenities = random.sample(default_amenities, random.randint(1, 3))
    
    # Generate neighborhood features based on location
    neighborhood_features = []
    if 'New York' in location:
        neighborhood_features = ['subway_access', 'restaurants', 'shopping', 'museums']
    elif 'San Francisco' in location:
        neighborhood_features = ['tech_hub', 'public_transport', 'parks', 'restaurants']
    elif 'Los Angeles' in location:
        neighborhood_features = ['entertainment_district', 'beaches', 'highways', 'dining']
    elif 'Miami' in location:
        neighborhood_features = ['beach_access', 'nightlife', 'international_cuisine', 'boating']
    elif 'Austin' in location:
        neighborhood_features = ['music_scene', 'food_trucks', 'tech_companies', 'outdoor_activities']
    elif 'Chicago' in location:
        neighborhood_features = ['lakefront', 'architecture', 'public_transport', 'cultural_events']
    elif 'Dallas' in location:
        neighborhood_features = ['business_district', 'shopping_centers', 'good_schools', 'family_friendly']
    elif 'Seattle' in location:
        neighborhood_features = ['tech_hub', 'coffee_culture', 'mountains', 'waterfront']
    elif 'Boston' in location:
        neighborhood_features = ['historic_district', 'universities', 'walkable', 'public_transport']
    else:
        neighborhood_features = ['good_schools', 'quiet_neighborhood', 'family_friendly']
    
    # Create comprehensive property data
    property_data = {
        "id": property_id,
        "title": title,
        "address": full_address,
        "property_type": property_type,
        "lot_size": lot_size,
        "square_footage": square_footage,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "garage": 1 if any('garage' in a.lower() or 'parking' in a.lower() for a in amenities) else random.randint(0, 2),
        "year_built": year_built,
        "market_value": price,
        "last_sold_price": last_sold_price,
        "last_sold_date": last_sold_date.strftime('%Y-%m-%d'),
        "property_tax": property_tax,
        "hoa_fee": hoa_fee,
        "amenities": standardized_amenities,
        "neighborhood_features": neighborhood_features,
        "condition": random.choice(['excellent', 'good', 'good', 'fair']),  # Weighted toward good
        "city": city,
        "state": state,
        "neighborhood": f"{city} Central" if 'downtown' in title.lower() else f"{city} Residential",
        "image_url": image_data.get('image_url', ''),
        "features": [
            title,
            f"{bedrooms} bedrooms, {bathrooms} bathrooms",
            f"{size_sqft:,} sq ft",
            f"Built in {year_built}"
        ] + amenities[:3],  # Include top 3 amenities as features
        "nearby_amenities": [
            f"Shopping center - 0.{random.randint(2, 8)} miles",
            f"Public transportation - 0.{random.randint(1, 5)} miles",
            f"School - 0.{random.randint(2, 6)} miles",
            f"Hospital - {random.randint(1, 3)}.{random.randint(0, 9)} miles"
        ]
    }
    
    return property_data

def convert_and_merge_json_files():
    """Convert and merge the three JSON files into comprehensive property data"""
    print("🏠 CONVERTING AND MERGING JSON FILES")
    print("=" * 50)
    
    # Load all three JSON files
    json1_data = load_json_txt_file('dataset/JSON 1.txt')
    json2_data = load_json_txt_file('dataset/JSON 2.txt')
    json3_data = load_json_txt_file('dataset/JSON 3.txt')
    
    if not json1_data:
        print("❌ Could not load JSON 1.txt")
        return False
    
    print(f"📁 Loaded {len(json1_data)} properties from JSON 1.txt")
    print(f"📁 Loaded {len(json2_data)} property details from JSON 2.txt")  
    print(f"📁 Loaded {len(json3_data)} property images from JSON 3.txt")
    
    # Create merged property data
    merged_properties = []
    
    for i, base_property in enumerate(json1_data):
        property_id = base_property.get('id', i + 1)
        
        # Find matching details and image by ID
        details = next((d for d in json2_data if d.get('id') == property_id), {})
        image_data = next((img for img in json3_data if img.get('id') == property_id), {})
        
        # Generate comprehensive property data
        property_data = generate_default_property_data(property_id, base_property, details, image_data)
        merged_properties.append(property_data)
        
        print(f"✅ Processed: {property_data['title']} - ${property_data['market_value']:,} ({property_data['address']})")
    
    # Save merged properties to new JSON files in the properties directory
    properties_dir = 'dataset/properties'
    os.makedirs(properties_dir, exist_ok=True)
    
    saved_count = 0
    for prop in merged_properties:
        # Create filename from address
        address_clean = prop['address'].replace(' ', '_').replace(',', '').replace('.', '').lower()
        filename = f"{address_clean[:50]}.json"  # Limit filename length
        filepath = os.path.join(properties_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(prop, f, indent=2, ensure_ascii=False)
            saved_count += 1
            print(f"💾 Saved: {filename}")
        except Exception as e:
            print(f"❌ Error saving {filename}: {e}")
    
    # Create or update property index
    index_file = 'dataset/property_index.json'
    index_data = {
        "properties": [
            {
                "id": prop["id"],
                "address": prop["address"],
                "property_type": prop["property_type"],
                "market_value": prop["market_value"],
                "bedrooms": prop["bedrooms"],
                "bathrooms": prop["bathrooms"],
                "image_url": prop["image_url"]
            }
            for prop in merged_properties
        ],
        "total_properties": len(merged_properties),
        "last_updated": datetime.now().isoformat()
    }
    
    try:
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)
        print(f"📊 Updated property index: {index_file}")
    except Exception as e:
        print(f"❌ Error creating index: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 CONVERSION SUMMARY")
    print(f"✅ Properties processed: {len(merged_properties)}")
    print(f"💾 Files saved: {saved_count}")
    print(f"📍 Average price: ${sum(p['market_value'] for p in merged_properties) / len(merged_properties):,.0f}")
    
    property_types = {}
    for prop in merged_properties:
        ptype = prop['property_type']
        property_types[ptype] = property_types.get(ptype, 0) + 1
    print(f"🏠 Property types: {property_types}")
    
    print("\n🎉 All your JSON data has been converted and is ready for comparison!")
    print("🚀 Restart the backend to load the new property data.")
    
    return True

if __name__ == "__main__":
    # Run the conversion
    success = convert_and_merge_json_files()
    
    if success:
        print("\n💡 Next steps:")
        print("   1. Restart backend: cd backend && python main.py")
        print("   2. Start frontend: cd frontend && npm start") 
        print("   3. Go to 'Manage Database' tab to see all properties")
        print("   4. Select any 2 properties to compare them!")
        print("   5. All properties now include images and detailed data!")
    else:
        print("\n🔧 Please check that the JSON files exist and try again.")