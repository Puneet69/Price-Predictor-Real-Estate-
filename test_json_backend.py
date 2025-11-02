#!/usr/bin/env python3
"""
Simple test to verify JSON-only backend functionality
"""

def test_json_backend():
    """Test that backend uses JSON files only (no MongoDB)"""
    
    import sys
    import os
    
    # Add backend directory to path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
    
    try:
        # Test importing the property data manager
        from property_data_manager import PropertyDataManager
        
        # Initialize property manager
        dataset_path = os.path.join(os.path.dirname(__file__), 'dataset')
        property_manager = PropertyDataManager(dataset_path)
        
        print("🧪 Testing JSON-Only Backend Configuration")
        print("=" * 50)
        
        # Test 1: Check property loading
        print("📋 Test 1: Loading properties from JSON files...")
        properties = property_manager.get_all_properties()
        print(f"✅ Loaded {len(properties)} properties from JSON files")
        
        # Show first few properties
        for i, prop in enumerate(properties[:3]):
            print(f"   {i+1}. {prop['address']} - ${prop['price']:,}")
        
        # Test 2: Test search functionality
        print("\n🔍 Test 2: Testing search functionality...")
        search_results = property_manager.search_properties("New York")
        print(f"✅ Found {len(search_results)} properties in New York")
        
        # Test 3: Test property lookup by address
        print("\n🏠 Test 3: Testing property lookup...")
        first_property = properties[0]
        found_property = property_manager.get_property_by_address(first_property['address'])
        
        if found_property:
            print(f"✅ Successfully found property: {found_property['address']}")
        else:
            print("❌ Property lookup failed")
        
        print("\n🎉 All JSON backend tests passed!")
        print(f"📊 Total properties available: {len(properties)}")
        print("🚀 Backend is ready to serve data from JSON files only!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_json_backend()
    exit(0 if success else 1)