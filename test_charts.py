#!/usr/bin/env python3
"""
Test script to verify chart generation functionality
"""
import requests
import json
import base64
from io import BytesIO
from PIL import Image

def test_chart_generation():
    """Test the chart generation by making a comparison request"""
    
    # Test data - compare two properties
    test_data = {
        "property_ids": ["property_1", "property_2"]
    }
    
    print("🧪 Testing Property Comparison App with Chart Generation...")
    print("=" * 60)
    
    try:
        # Test 1: Get all properties
        print("📋 Test 1: Fetching all properties...")
        response = requests.get("http://localhost:8000/properties")
        if response.status_code == 200:
            properties = response.json()
            print(f"✅ Found {len(properties)} properties")
            
            # Show first few properties
            for i, prop in enumerate(properties[:3]):
                print(f"   {i+1}. {prop['address']} - ${prop['price']:,}")
        else:
            print(f"❌ Failed to fetch properties: {response.status_code}")
            return
        
        # Test 2: Get property statistics
        print("\n📊 Test 2: Fetching property statistics...")
        response = requests.get("http://localhost:8000/properties/stats/summary")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Property Statistics:")
            print(f"   Average Price: ${stats['average_price']:,.0f}")
            print(f"   Price Range: ${stats['min_price']:,} - ${stats['max_price']:,}")
        else:
            print(f"❌ Failed to fetch statistics: {response.status_code}")
        
        # Test 3: Compare properties with chart generation
        print("\n🏠 Test 3: Comparing properties with chart generation...")
        if len(properties) >= 2:
            # Use the first two properties for comparison
            comparison_data = {
                "property_ids": [properties[0]['id'], properties[1]['id']]
            }
            
            response = requests.post(
                "http://localhost:8000/compare-properties",
                json=comparison_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Property comparison successful!")
                print(f"   Comparing: {properties[0]['address']} vs {properties[1]['address']}")
                print(f"   Price difference: ${abs(result['price_difference']):,}")
                
                # Check if chart was generated
                if 'chart' in result and result['chart']:
                    print("📈 Chart generated successfully!")
                    
                    # Try to decode and verify the chart image
                    try:
                        chart_data = result['chart'].split(',')[1]  # Remove data:image/png;base64,
                        image_bytes = base64.b64decode(chart_data)
                        image = Image.open(BytesIO(image_bytes))
                        print(f"   Chart dimensions: {image.size[0]}x{image.size[1]} pixels")
                        print(f"   Chart format: {image.format}")
                        
                        # Save chart for inspection (optional)
                        image.save("/Users/puneet/Desktop/Case Study 2/test_chart.png")
                        print("   📁 Chart saved as test_chart.png")
                        
                    except Exception as e:
                        print(f"⚠️  Chart data present but couldn't decode: {e}")
                else:
                    print("⚠️  No chart data in response")
                    
            else:
                print(f"❌ Failed to compare properties: {response.status_code}")
                print(f"   Response: {response.text}")
        
        print("\n🎉 All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    test_chart_generation()