#!/usr/bin/env python3
"""
Test Property Data Integration
Test that the property JSON files are properly loaded and accessible
"""

import requests
import json

def test_api_endpoints():
    """Test the API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 TESTING PROPERTY DATA INTEGRATION")
    print("=" * 50)
    
    # Test health endpoint
    print("\n1. Testing Health Endpoint:")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print("   ✅ Health check passed")
            print(f"   📊 Data sources:")
            print(f"      MongoDB: {health_data.get('data_sources', {}).get('mongodb', {})}")
            print(f"      JSON Files: {health_data.get('data_sources', {}).get('json_files', {})}")
            print(f"   🎯 Primary source: {health_data.get('primary_data_source', 'unknown')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test properties endpoint
    print("\n2. Testing Properties Endpoint:")
    try:
        response = requests.get(f"{base_url}/properties")
        if response.status_code == 200:
            props_data = response.json()
            properties = props_data.get('properties', [])
            print(f"   ✅ Properties loaded: {len(properties)}")
            print(f"   📂 Source: {props_data.get('source', 'unknown')}")
            
            for i, prop in enumerate(properties, 1):
                address = prop.get('address', 'Unknown')
                price = prop.get('market_value', 0)
                prop_type = prop.get('property_type', 'Unknown')
                print(f"   {i}. {address} - ${price:,} ({prop_type})")
        else:
            print(f"   ❌ Properties endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Properties endpoint error: {e}")
        return False
    
    # Test stats endpoint
    print("\n3. Testing Stats Endpoint:")
    try:
        response = requests.get(f"{base_url}/properties/stats/summary")
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ Stats retrieved")
            print(f"   📊 Total properties: {stats.get('total_properties', 0)}")
            print(f"   🏠 Property types: {stats.get('property_types', {})}")
            print(f"   💰 Average value: ${stats.get('average_market_value', 0):,.2f}")
            print(f"   📂 Source: {stats.get('source', 'unknown')}")
        else:
            print(f"   ❌ Stats endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Stats endpoint error: {e}")
    
    # Test search endpoint
    print("\n4. Testing Search Endpoint:")
    try:
        response = requests.get(f"{base_url}/properties/search?query=San Francisco")
        if response.status_code == 200:
            search_data = response.json()
            results = search_data.get('properties', [])
            print(f"   ✅ Search completed: {len(results)} results for 'San Francisco'")
            
            for result in results:
                address = result.get('address', 'Unknown')
                print(f"      - {address}")
        else:
            print(f"   ❌ Search endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Search endpoint error: {e}")
    
    # Test comparison endpoint
    if len(properties) >= 2:
        print("\n5. Testing Property Comparison:")
        try:
            address1 = properties[0].get('address', '')
            address2 = properties[1].get('address', '')
            
            comparison_data = {
                "address1": address1,
                "address2": address2
            }
            
            response = requests.post(
                f"{base_url}/compare-properties-mongo",
                json=comparison_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                comparison = response.json()
                print(f"   ✅ Comparison completed")
                print(f"   🏠 Property 1: {address1}")
                print(f"      Price: ${comparison.get('property1', {}).get('predicted_price', 0):,}")
                print(f"   🏠 Property 2: {address2}")
                print(f"      Price: ${comparison.get('property2', {}).get('predicted_price', 0):,}")
                print(f"   💰 Price difference: ${comparison.get('price_difference', 0):,}")
                print(f"   🎯 Higher priced: {comparison.get('higher_priced', 'Unknown')}")
                print(f"   📂 Source: {comparison.get('source', 'unknown')}")
            else:
                print(f"   ❌ Comparison failed: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Comparison error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API Integration Test Completed!")
    print("\n💡 Next Steps:")
    print("   1. Start the frontend: cd frontend && npm start")
    print("   2. Open http://localhost:3000")
    print("   3. Click 'Manage Database' tab")
    print("   4. You should see your JSON properties loaded!")
    print("   5. Select any two properties and click 'Compare Properties'")
    
    return True

if __name__ == "__main__":
    test_api_endpoints()