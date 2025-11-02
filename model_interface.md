# Model Interface Documentation - complex_price_model_v2.pkl

## Input Schema

The ML model expects a dictionary with the following EXACT format:

```python
{
    "property_type": str,     # "SFH" OR "Condo" ONLY (no "Townhouse")
    "lot_area": int,          # Used ONLY if property_type == "SFH"
    "building_area": int,     # Used ONLY if property_type == "Condo"  
    "bedrooms": int,          # Number of bedrooms
    "bathrooms": int,         # Number of bathrooms
    "year_built": int,        # Year the property was built
    "has_pool": bool,         # True/False
    "has_garage": bool,       # True/False
    "school_rating": int      # Rating from 1-10
}
```

## Schema Rules

**CRITICAL**: The model uses different area fields based on property type:
- **SFH Properties**: Use `lot_area` (set `building_area = 0`)
- **Condo Properties**: Use `building_area` (set `lot_area = 0`)

## Usage Examples

### Single Family Home (SFH)
```python
import pickle

# Load the model
with open('complex_price_model_v2.pkl', 'rb') as f:
    model = pickle.load(f)

# SFH property data
sfh_data = {
    "property_type": "SFH",
    "lot_area": 5000,        # Used for SFH
    "building_area": 0,      # Not used for SFH
    "bedrooms": 3,
    "bathrooms": 2,
    "year_built": 2015,
    "has_pool": True,
    "has_garage": False,
    "school_rating": 9
}

prediction = model.predict([sfh_data])
print(f"SFH Predicted price: ${prediction[0]:,.2f}")
```

### Condo Property
```python
# Condo property data
condo_data = {
    "property_type": "Condo",
    "lot_area": 0,           # Not used for Condo
    "building_area": 1200,   # Used for Condo
    "bedrooms": 2,
    "bathrooms": 2,
    "year_built": 2018,
    "has_pool": False,
    "has_garage": True,
    "school_rating": 8
}

prediction = model.predict([condo_data])
print(f"Condo Predicted price: ${prediction[0]:,.2f}")
```

## Notes

- ✅ Model accepts **ONLY** "SFH" or "Condo" property types
- ✅ Area fields are mutually exclusive based on property type
- ✅ All other fields are used for both property types
- ✅ The model returns a price prediction in USD
- ⚠️ Input validation is critical for accurate predictions