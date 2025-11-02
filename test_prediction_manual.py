#!/usr/bin/env python3
"""
Simple manual test of the AI prediction logic
"""

import json
import random

# Simulate the predict_price function logic
def test_predict_price():
    print("🧪 Testing AI Prediction Logic Manually")
    print("=" * 50)
    
    # Sample property data like our MongoDB would have
    test_properties = [
        {
            "address": "123 Oak Street, Austin, TX",
            "property_type": "SFH",
            "square_footage": 2500,
            "lot_size": 8000,
            "bedrooms": 4,
            "bathrooms": 3,
            "year_built": 2010,
            "condition": "excellent",
            "amenities": ["pool", "garage"],
            "market_value": 1200000
        },
        {
            "address": "456 Pine Avenue, Austin, TX", 
            "property_type": "Condo",
            "square_footage": 1800,
            "bedrooms": 3,
            "bathrooms": 2,
            "year_built": 2005,
            "condition": "fair",
            "amenities": ["garage"],
            "market_value": 850000
        }
    ]
    
    for i, prop in enumerate(test_properties, 1):
        print(f"\n🏠 Property {i}: {prop['address']}")
        print(f"   Market Value: ${prop['market_value']:,}")
        print(f"   Condition: {prop['condition']}")
        
        # Manual AI prediction calculation
        area = prop.get("square_footage", 2000)
        
        if prop.get("property_type") == "SFH":
            base_price = area * 80
        else:
            base_price = area * 250
            
        # Room factors
        bedrooms = prop.get("bedrooms", 2)
        bathrooms = prop.get("bathrooms", 2)
        room_bonus = (bedrooms * 35000) + (bathrooms * 25000)
        
        # Age factor
        year_built = prop.get("year_built", 2000)
        age = 2024 - year_built
        if age < 5:
            year_bonus = 80000
        elif age < 15:
            year_bonus = 50000
        else:
            year_bonus = 20000
            
        # Amenities
        amenities = prop.get("amenities", [])
        pool_bonus = 65000 if "pool" in amenities else 0
        garage_bonus = 40000 if "garage" in amenities else 0
        
        # School rating (default)
        school_bonus = 6 * 15000
        
        # Condition multiplier
        condition = prop.get("condition", "fair").lower()
        condition_multipliers = {
            "excellent": 1.15,
            "very good": 1.08,
            "good": 1.02,
            "fair": 0.95,
            "poor": 0.80
        }
        condition_mult = condition_multipliers.get(condition, 0.95)
        
        # Calculate prediction
        predicted_price = (base_price + room_bonus + year_bonus + pool_bonus + 
                          garage_bonus + school_bonus) * condition_mult
        
        print(f"   AI Calculation:")
        print(f"     Base ({area} sq ft): ${base_price:,}")
        print(f"     Rooms bonus: ${room_bonus:,}")
        print(f"     Age bonus: ${year_bonus:,}")
        print(f"     Pool bonus: ${pool_bonus:,}")
        print(f"     Garage bonus: ${garage_bonus:,}")
        print(f"     School bonus: ${school_bonus:,}")
        print(f"     Condition ({condition}): x{condition_mult}")
        print(f"   AI Predicted: ${predicted_price:,.0f}")
        
        # Check if same
        is_same = abs(predicted_price - prop['market_value']) < 1000
        print(f"   Same as market? {'YES' if is_same else 'NO'}")
        
        if not is_same:
            diff = predicted_price - prop['market_value']
            print(f"   Difference: ${diff:+,.0f}")

if __name__ == "__main__":
    test_predict_price()