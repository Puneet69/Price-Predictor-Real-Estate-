# 🏠 Property Dataset

This folder contains custom property data for the Property Comparison App.

## 📁 Folder Structure

```
dataset/
├── properties/                 # Individual property JSON files
│   ├── 123_main_street_sf.json
│   ├── 456_oak_avenue_la.json
│   ├── 789_pine_road_seattle.json
│   └── 321_elm_street_nyc.json
├── neighborhoods/              # Future: Neighborhood data
├── property_index.json         # Index of all properties
├── property_loader.py          # Python loader module
├── property_template.json      # Template for new properties
└── README.md                   # This file
```

## ✅ **Pre-loaded Properties**

The dataset comes with 4 sample properties:

1. **123 Main Street, San Francisco, CA** - SFH, $1,250,000
2. **456 Oak Avenue, Los Angeles, CA** - Condo, $950,000  
3. **789 Pine Road, Seattle, WA** - SFH, $850,000
4. **321 Elm Street, New York, NY** - Condo, $750,000

## 📝 **Adding New Properties**

### Method 1: Copy Template
1. Copy `property_template.json`
2. Rename to descriptive filename (e.g., `555_broadway_nyc.json`)
3. Fill in all property details
4. Save in `properties/` folder
5. Update `property_index.json`

### Method 2: Use the Schema
Create a new JSON file with this structure:

```json
{
  "address": "555 Broadway, New York, NY 10012",
  "property_type": "SFH",
  "lot_area": 3500,
  "building_area": 0,
  "bedrooms": 3,
  "bathrooms": 2,
  "year_built": 2018,
  "has_pool": false,
  "has_garage": true,
  "school_rating": 8,
  "neighborhood": "SoHo",
  "city": "New York",
  "state": "NY",
  "zip_code": "10012",
  "market_value": 1500000,
  "last_sold_date": "2024-03-15",
  "last_sold_price": 1400000,
  "property_tax": 25000,
  "hoa_fee": 0,
  "features": [
    "Renovated kitchen",
    "Rooftop deck",
    "Exposed brick"
  ],
  "nearby_amenities": [
    "Subway station - 0.1 miles",
    "Central Park - 1.2 miles",
    "Shopping district - 0.3 miles"
  ]
}
```

## 🔧 **Required Fields for ML Model**

These fields are **required** for the ML model compatibility:

- `property_type`: Must be "SFH" or "Condo"
- `lot_area`: Used only for SFH (set to 0 for Condos)
- `building_area`: Used only for Condos (set to 0 for SFH)
- `bedrooms`: Number of bedrooms (1-5)
- `bathrooms`: Number of bathrooms (1-4)
- `year_built`: Year property was built
- `has_pool`: true/false
- `has_garage`: true/false  
- `school_rating`: Rating from 1-10

## 🎯 **Address Matching**

The system uses fuzzy matching to find properties. These addresses will match:

- "123 Main Street, San Francisco, CA"
- "123 Main St, San Francisco, CA"  
- "123 main street san francisco ca"
- "123 Main St SF CA"

## 📊 **Testing Your Data**

To test if your property data loads correctly:

```bash
cd dataset
python property_loader.py
```

## 🚀 **Using in the App**

1. Add your JSON files to `properties/` folder
2. Restart the backend server
3. Enter the property address in the web app
4. The app will automatically use your custom data!

## 📈 **Data Priority**

The app uses this priority order:
1. **Custom JSON files** (this dataset)
2. **Simulated data** (fallback if no JSON found)

## 💡 **Tips for Best Results**

- Use exact addresses that users will search for
- Include common abbreviations in the index
- Set `lot_area=0` for Condos, `building_area=0` for SFH
- School ratings should be 1-10 scale
- Market values help with price predictions
- Features and amenities enhance the user experience

## 🔮 **Future Enhancements**

- Neighborhood average data
- Historical price trends
- Property images
- Nearby schools database
- Crime statistics
- Walk scores

Your custom property dataset is now ready to use! 🏠✨