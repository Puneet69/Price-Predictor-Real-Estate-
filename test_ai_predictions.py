#!/usr/bin/env python3
"""
Test script to verify AI predictions are different from market values
"""

import requests
import json

def test_ai_predictions():
    base_url = "http://localhost:8000"
    
    # Test data - two properties with different conditions
    test_comparison = {
        "address1": "123 Oak Street, Austin, TX 78701",
        "address2": "456 Pine Avenue, Austin, TX 78702"
    }
    
    print("🧪 Testing AI Prediction vs Market Value Differences")
    print("=" * 60)
    
    try:
        # Make comparison request
        response = requests.post(
            f"{base_url}/compare-properties",
            json=test_comparison,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract property data
            prop1 = data["property1"]
            prop2 = data["property2"]
            
            print(f"🏠 Property 1: {prop1['address']}")
            print(f"   Market Value: ${prop1.get('market_value', 0):,.0f}")
            print(f"   AI Predicted: ${prop1.get('predicted_price', 0):,.0f}")
            print(f"   Condition: {prop1.get('condition', 'N/A')}")
            print(f"   Difference: ${abs(prop1.get('market_value', 0) - prop1.get('predicted_price', 0)):,.0f}")
            print()
            
            print(f"🏠 Property 2: {prop2['address']}")
            print(f"   Market Value: ${prop2.get('market_value', 0):,.0f}")
            print(f"   AI Predicted: ${prop2.get('predicted_price', 0):,.0f}")
            print(f"   Condition: {prop2.get('condition', 'N/A')}")
            print(f"   Difference: ${abs(prop2.get('market_value', 0) - prop2.get('predicted_price', 0)):,.0f}")
            print()
            
            # Check if predictions are different
            prop1_diff = prop1.get('market_value', 0) != prop1.get('predicted_price', 0)
            prop2_diff = prop2.get('market_value', 0) != prop2.get('predicted_price', 0)
            
            if prop1_diff and prop2_diff:
                print("✅ SUCCESS: AI predictions are different from market values!")
            else:
                print("❌ ISSUE: AI predictions are same as market values")
                print("   This means the AI model is not calculating independent predictions")
            
            print("\n📊 Analysis Summary:")
            print(f"   Property 1 - AI vs Market: {'Different' if prop1_diff else 'Same'}")
            print(f"   Property 2 - AI vs Market: {'Different' if prop2_diff else 'Same'}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Backend server is not running!")
        print("   Please start the backend first: python backend/main.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ai_predictions()