#!/usr/bin/env python3
"""
Quick test to debug AI prediction issue
"""

import requests
import json
import sys

def test_backend():
    print("🧪 Testing AI Prediction vs Market Value")
    print("=" * 50)
    
    # Test if backend is running
    try:
        health = requests.get("http://localhost:8000/health", timeout=5)
        if health.status_code != 200:
            print("❌ Backend not healthy")
            return
        print("✅ Backend is running")
    except:
        print("❌ Backend is not running! Start it with: cd backend && python main.py")
        return
    
    # Get sample properties first
    try:
        props_response = requests.get("http://localhost:8000/properties?limit=5")
        if props_response.status_code == 200:
            props_data = props_response.json()
            if len(props_data['properties']) >= 2:
                addr1 = props_data['properties'][0]['address']
                addr2 = props_data['properties'][1]['address']
                print(f"🏠 Using properties:")
                print(f"   1. {addr1}")
                print(f"   2. {addr2}")
            else:
                print("❌ Not enough properties in database")
                return
        else:
            print("❌ Could not get properties list")
            return
    except Exception as e:
        print(f"❌ Error getting properties: {e}")
        return
    
    # Test comparison
    try:
        comparison_data = {
            "address1": addr1,
            "address2": addr2
        }
        
        print(f"\n🔄 Testing comparison...")
        response = requests.post(
            "http://localhost:8000/compare-properties",
            json=comparison_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            prop1 = data['property1']
            prop2 = data['property2']
            
            print(f"\n📊 RESULTS:")
            print(f"🏠 Property 1: {prop1['address']}")
            print(f"   Market Value: ${prop1.get('market_value', 0):,}")
            print(f"   AI Predicted: ${prop1.get('predicted_price', 0):,}")
            print(f"   Same? {'YES' if prop1.get('market_value') == prop1.get('predicted_price') else 'NO'}")
            print(f"   Condition: {prop1.get('condition', 'N/A')}")
            
            print(f"\n🏠 Property 2: {prop2['address']}")
            print(f"   Market Value: ${prop2.get('market_value', 0):,}")
            print(f"   AI Predicted: ${prop2.get('predicted_price', 0):,}")
            print(f"   Same? {'YES' if prop2.get('market_value') == prop2.get('predicted_price') else 'NO'}")
            print(f"   Condition: {prop2.get('condition', 'N/A')}")
            
            # Check if they're the same
            same1 = prop1.get('market_value') == prop1.get('predicted_price')
            same2 = prop2.get('market_value') == prop2.get('predicted_price')
            
            if same1 or same2:
                print(f"\n❌ ISSUE CONFIRMED: AI predictions are same as market values")
                print(f"   This indicates the prediction algorithm needs fixing")
            else:
                print(f"\n✅ SUCCESS: AI predictions are different from market values!")
        else:
            print(f"❌ Comparison failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Comparison error: {e}")

if __name__ == "__main__":
    test_backend()