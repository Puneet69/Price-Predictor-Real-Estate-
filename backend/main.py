from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import random
from typing import Dict, Any, List, Optional
import os
import sys
import base64
from io import BytesIO

# Graph generation imports
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np
    GRAPHING_AVAILABLE = True
    print("✅ Graph generation libraries loaded")
except ImportError as e:
    print(f"Warning: Graph libraries not available: {e}")
    GRAPHING_AVAILABLE = False

# Add dataset directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dataset'))

# Skip the problematic PropertyDatasetLoader for now
dataset_loader = None
print("ℹ️  Using hybrid JSON + MongoDB system")

# Import MongoDB storage for custom properties
try:
    from mongodb_storage import PropertyMongoStorage
    # Use environment variable for MongoDB URL in production
    mongodb_url = os.getenv('MONGODB_URI', 'mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate')
    mongo_storage = PropertyMongoStorage(connection_string=mongodb_url)
    print("✅ MongoDB storage initialized for custom properties")
except ImportError as e:
    print(f"Warning: Could not load MongoDB storage: {e}")
    mongo_storage = None

# Import Property Data Manager (JSON files for base properties)
try:
    from property_data_manager import PropertyDataManager
    property_manager = PropertyDataManager(os.path.join(os.path.dirname(__file__), '..', 'dataset'))
    print("✅ Property data manager initialized with JSON files")
except ImportError as e:
    print(f"Warning: Could not load property data manager: {e}")
    property_manager = None

# Pydantic models for request/response
class PropertyCreate(BaseModel):
    address: str
    property_type: str
    lot_size: Optional[int] = 0
    square_footage: Optional[int] = 0
    bedrooms: Optional[int] = 0
    bathrooms: Optional[int] = 0
    garage: Optional[int] = 0
    year_built: Optional[int] = 2000
    market_value: Optional[int] = 0
    amenities: Optional[List[str]] = []
    neighborhood_features: Optional[List[str]] = []
    condition: Optional[str] = "fair"

class PropertySearch(BaseModel):
    query: Optional[str] = ""
    property_type: Optional[str] = ""
    min_price: Optional[int] = 0
    max_price: Optional[int] = 999999999
    limit: Optional[int] = 50

app = FastAPI(title="Property Comparison API", version="1.0.0")

# Enable CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the ML model
model = None
try:
    import pickle
    with open('complex_price_model_v2.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Warning: Could not load model: {e}")
    print("App will work with fallback pricing algorithm")

def sync_json_to_mongodb():
    """Sync JSON properties to MongoDB on startup"""
    if not mongo_storage or not property_manager:
        print("⚠️  Cannot sync: MongoDB or PropertyManager not available")
        return
    
    try:
        if not mongo_storage.is_connected():
            print("⚠️  MongoDB not connected, skipping sync")
            return
            
        print("🔄 Syncing JSON properties to MongoDB...")
        json_properties = property_manager.get_all_properties()
        synced_count = 0
        
        for prop in json_properties:
            # Check if property already exists in MongoDB
            existing = mongo_storage.get_property_by_address(prop['address'])
            if not existing:
                # Add property to MongoDB with source marker
                prop_with_source = prop.copy()
                prop_with_source['source'] = 'json_file'
                prop_with_source['is_custom'] = False
                
                success = mongo_storage.add_property(prop_with_source)
                if success:
                    synced_count += 1
        
        print(f"✅ Synced {synced_count} properties from JSON to MongoDB")
        total_in_mongo = len(mongo_storage.get_all_properties())
        print(f"📊 Total properties in MongoDB: {total_in_mongo}")
        
    except Exception as e:
        print(f"❌ Error syncing JSON to MongoDB: {e}")

# Sync JSON properties to MongoDB on startup
sync_json_to_mongodb()

def get_property_data(address: str) -> Dict[str, Any]:
    """
    Get property data from custom dataset or generate mock data as fallback.
    First tries to load from JSON files, then falls back to simulation.
    """
    # Try to load from custom dataset first
    if dataset_loader:
        real_data = dataset_loader.load_property_data(address)
        if real_data:
            # Extract ML model compatible data + additional display fields
            return {
                "property_type": real_data.get("property_type", "SFH"),
                "lot_area": real_data.get("lot_area", 0),
                "building_area": real_data.get("building_area", 0), 
                "bedrooms": real_data.get("bedrooms", 2),
                "bathrooms": real_data.get("bathrooms", 2),
                "year_built": real_data.get("year_built", 2000),
                "has_pool": real_data.get("has_pool", False),
                "has_garage": real_data.get("has_garage", False),
                "school_rating": real_data.get("school_rating", 5),
                # Additional fields for enhanced display
                "market_value": real_data.get("market_value"),
                "neighborhood": real_data.get("neighborhood"),
                "features": real_data.get("features", []),
                "nearby_amenities": real_data.get("nearby_amenities", []),
                "last_sold_price": real_data.get("last_sold_price"),
                "property_tax": real_data.get("property_tax"),
                "hoa_fee": real_data.get("hoa_fee", 0)
            }
    
    # Fallback to simulated data
    print(f"⚠️  Using simulated data for: {address}")
    return simulate_property_data(address)

def simulate_property_data(address: str) -> Dict[str, Any]:
    """
    Simulate property data extraction from an address.
    In a real app, this would scrape from Zillow, Redfin, or use a real estate API.
    
    Schema matches complex_price_model_v2.pkl requirements:
    - property_type: "SFH" or "Condo" only
    - lot_area: used only for SFH properties  
    - building_area: used only for Condo properties
    """
    # Generate realistic mock data based on address
    hash_seed = hash(address) % 1000
    random.seed(hash_seed)  # Consistent data for same address
    
    # Model only accepts "SFH" or "Condo" (no "Townhouse")
    property_types = ["SFH", "Condo"]
    property_type = random.choice(property_types)
    
    # Base property data
    data = {
        "property_type": property_type,
        "bedrooms": random.randint(1, 5),
        "bathrooms": random.randint(1, 4),
        "year_built": random.randint(1950, 2023),
        "has_pool": random.choice([True, False]),
        "has_garage": random.choice([True, False]),
        "school_rating": random.randint(1, 10)
    }
    
    # Add area fields based on property type (model schema requirement)
    if property_type == "SFH":
        data["lot_area"] = random.randint(2000, 15000)
        data["building_area"] = 0  # Not used for SFH in model
    else:  # Condo
        data["lot_area"] = 0  # Not used for Condo in model
        data["building_area"] = random.randint(800, 4000)
    
    return data

def generate_comparison_chart(property1: Dict[str, Any], property2: Dict[str, Any]) -> str:
    """Generate comparison chart and return base64 encoded image"""
    if not GRAPHING_AVAILABLE:
        return None
    
    try:
        # Set up the plotting style
        plt.style.use('default')
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Property Comparison Dashboard', fontsize=16, fontweight='bold')
        
        # Colors
        colors = ['#3B82F6', '#EF4444']  # Blue and Red
        property_names = ['Property 1', 'Property 2']
        
        # 1. Price Comparison Bar Chart
        prices = [
            property1.get('market_value') or property1.get('display_price', 0),
            property2.get('market_value') or property2.get('display_price', 0)
        ]
        bars1 = ax1.bar(property_names, prices, color=colors, alpha=0.8)
        ax1.set_title('Market Value Comparison', fontweight='bold', pad=20)
        ax1.set_ylabel('Price ($)')
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Add value labels on bars
        for bar, price in zip(bars1, prices):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + max(prices)*0.02,
                    f'${price:,.0f}', ha='center', va='bottom', fontweight='bold')
        
        # 2. Property Features Radar Chart
        features = ['Bedrooms', 'Bathrooms', 'Year Built\n(Normalized)', 'Property Tax\n(Normalized)']
        
        # Normalize values for radar chart
        prop1_values = [
            property1.get('bedrooms', 0),
            property1.get('bathrooms', 0),
            min(10, (property1.get('year_built', 1950) - 1950) / 7.5),  # Normalize year built to 0-10 scale
            min(10, (property1.get('property_tax', 0) / 2000))  # Normalize property tax
        ]
        
        prop2_values = [
            property2.get('bedrooms', 0),
            property2.get('bathrooms', 0),
            min(10, (property2.get('year_built', 1950) - 1950) / 7.5),
            min(10, (property2.get('property_tax', 0) / 2000))
        ]
        
        x = np.arange(len(features))
        width = 0.35
        
        bars2_1 = ax2.bar(x - width/2, prop1_values, width, label='Property 1', color=colors[0], alpha=0.8)
        bars2_2 = ax2.bar(x + width/2, prop2_values, width, label='Property 2', color=colors[1], alpha=0.8)
        
        ax2.set_title('Property Features Comparison', fontweight='bold', pad=20)
        ax2.set_xticks(x)
        ax2.set_xticklabels(features, fontsize=9)
        ax2.legend()
        ax2.set_ylabel('Score/Count')
        
        # Add value labels
        for bars in [bars2_1, bars2_2]:
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{height:.1f}', ha='center', va='bottom', fontsize=8)
        
        # 3. Cost Analysis Pie Chart
        prop1_costs = []
        prop1_labels = []
        prop2_costs = []
        prop2_labels = []
        
        # Property 1 costs
        if property1.get('property_tax'):
            prop1_costs.append(property1['property_tax'])
            prop1_labels.append('Property Tax')
        if property1.get('hoa_fee'):
            prop1_costs.append(property1['hoa_fee'] * 12)  # Annual HOA
            prop1_labels.append('HOA (Annual)')
        
        # Property 2 costs
        if property2.get('property_tax'):
            prop2_costs.append(property2['property_tax'])
            prop2_labels.append('Property Tax')
        if property2.get('hoa_fee'):
            prop2_costs.append(property2['hoa_fee'] * 12)
            prop2_labels.append('HOA (Annual)')
        
        if prop1_costs:
            ax3.pie(prop1_costs, labels=prop1_labels, autopct='%1.1f%%', startangle=90, colors=['#3B82F6', '#60A5FA'])
            ax3.set_title('Property 1 - Annual Costs', fontweight='bold')
        else:
            ax3.text(0.5, 0.5, 'No cost data\navailable', ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Property 1 - Annual Costs', fontweight='bold')
        
        # 4. Investment Score Comparison
        def calculate_investment_score(prop):
            score = 0
            # Price per sq ft (lower is better)
            if prop.get('square_footage', 0) > 0 and prop.get('market_value', 0) > 0:
                price_per_sqft = prop['market_value'] / prop['square_footage']
                score += max(0, 10 - (price_per_sqft / 100))  # Normalize
            
            # Age of property (newer is better)
            if prop.get('year_built'):
                age = 2024 - prop['year_built']
                score += max(0, 10 - (age / 5))
            
            # School rating
            if prop.get('school_rating'):
                score += prop['school_rating']
            
            # Amenities count
            if prop.get('amenities'):
                score += min(5, len(prop['amenities']))
            
            return min(10, max(0, score))
        
        prop1_score = calculate_investment_score(property1)
        prop2_score = calculate_investment_score(property2)
        
        scores = [prop1_score, prop2_score]
        bars4 = ax4.bar(property_names, scores, color=colors, alpha=0.8)
        ax4.set_title('Investment Score (0-10)', fontweight='bold', pad=20)
        ax4.set_ylabel('Score')
        ax4.set_ylim(0, 10)
        
        # Add score labels
        for bar, score in zip(bars4, scores):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{score:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # Add recommendation
        if prop1_score > prop2_score:
            recommendation = "Property 1 Recommended"
            rec_color = colors[0]
        elif prop2_score > prop1_score:
            recommendation = "Property 2 Recommended"
            rec_color = colors[1]
        else:
            recommendation = "Both Properties Equal"
            rec_color = '#6B7280'
        
        fig.text(0.5, 0.02, f'🏆 {recommendation}', ha='center', va='bottom', 
                fontsize=14, fontweight='bold', color=rec_color)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.93, bottom=0.07)
        
        # Convert to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
        
    except Exception as e:
        print(f"Error generating chart: {e}")
        return None

def predict_price(property_data: Dict[str, Any]) -> float:
    """Use the ML model to predict property price"""
    if model is None:
        # Fallback: simple price estimation if model not available
        # Handle SFH vs Condo pricing differently
        if property_data["property_type"] == "SFH":
            base_price = property_data["lot_area"] * 50  # SFH uses lot_area
            area_multiplier = property_data["lot_area"]
        else:  # Condo
            base_price = property_data["building_area"] * 200  # Condo uses building_area
            area_multiplier = property_data["building_area"]
        
        room_bonus = (property_data["bedrooms"] + property_data["bathrooms"]) * 25000
        year_bonus = max(0, (property_data["year_built"] - 1970) * 1000)
        pool_bonus = 50000 if property_data["has_pool"] else 0
        garage_bonus = 30000 if property_data["has_garage"] else 0
        school_bonus = property_data["school_rating"] * 5000
        
        return base_price + room_bonus + year_bonus + pool_bonus + garage_bonus + school_bonus
    
    try:
        # Create model input that matches exact schema
        model_input = {
            "property_type": property_data["property_type"],
            "lot_area": property_data["lot_area"],
            "building_area": property_data["building_area"],
            "bedrooms": property_data["bedrooms"],
            "bathrooms": property_data["bathrooms"],
            "year_built": property_data["year_built"],
            "has_pool": property_data["has_pool"],
            "has_garage": property_data["has_garage"],
            "school_rating": property_data["school_rating"]
        }
        
        prediction = model.predict([model_input])
        return float(prediction[0]) if hasattr(prediction, '__iter__') else float(prediction)
    except Exception as e:
        print(f"Model prediction error: {e}")
        print(f"Model input was: {property_data}")
        # Fallback to simple estimation
        if property_data["property_type"] == "SFH":
            return property_data["lot_area"] * 100
        else:
            return property_data["building_area"] * 300

@app.get("/")
def read_root():
    return {"message": "Property Comparison API is running!"}

@app.post("/compare-properties")
async def compare_properties(request_data: dict):
    try:
        # Extract addresses from request
        address1 = request_data.get("address1", "").strip()
        address2 = request_data.get("address2", "").strip()
        
        if not address1 or not address2:
            raise HTTPException(status_code=400, detail="Both address1 and address2 are required")
        
        # Get property data from hybrid system (MongoDB with JSON + custom properties)
        property1_data = None
        property2_data = None
        
        # Try MongoDB first (has both JSON and custom properties)
        if mongo_storage and mongo_storage.is_connected():
            property1_data = mongo_storage.get_property_by_address(address1)
            property2_data = mongo_storage.get_property_by_address(address2)
        
        # Fallback to JSON files if not found in MongoDB
        if not property1_data and property_manager:
            property1_data = property_manager.get_property_by_address(address1)
        if not property2_data and property_manager:
            property2_data = property_manager.get_property_by_address(address2)
        
        # Final fallback to custom dataset loader
        if not property1_data:
            property1_data = get_property_data(address1)
        if not property2_data:
            property2_data = get_property_data(address2)
        
        # Use actual market value if available, otherwise predict price
        property1_price = property1_data.get("market_value") or predict_price(property1_data)
        property2_price = property2_data.get("market_value") or predict_price(property2_data)
        
        # Calculate accurate price difference
        price_diff = abs(property1_price - property2_price)
        percentage_diff = (price_diff / min(property1_price, property2_price)) * 100 if min(property1_price, property2_price) > 0 else 0
        
        # Create response objects with both actual and predicted prices
        property1 = {
            "address": address1,
            "market_value": property1_data.get("market_value"),
            "predicted_price": predict_price(property1_data) if not property1_data.get("market_value") else property1_data.get("market_value"),
            "display_price": property1_price,
            **property1_data
        }
        
        property2 = {
            "address": address2,
            "market_value": property2_data.get("market_value"),
            "predicted_price": predict_price(property2_data) if not property2_data.get("market_value") else property2_data.get("market_value"),
            "display_price": property2_price,
            **property2_data
        }
        
        # Generate comparison chart
        chart_base64 = generate_comparison_chart(property1, property2)
        
        return {
            "property1": property1,
            "property2": property2,
            "price_difference": price_diff,
            "percentage_difference": round(percentage_diff, 2),
            "higher_priced": address1 if property1_price > property2_price else address2,
            "comparison_summary": {
                "price_difference_formatted": f"${price_diff:,.0f}",
                "percentage_difference_formatted": f"{percentage_diff:.1f}%",
                "higher_property": address1 if property1_price > property2_price else address2,
                "lower_property": address2 if property1_price > property2_price else address1
            },
            "chart": chart_base64,
            "chart_available": chart_base64 is not None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing properties: {str(e)}")

@app.get("/health")
def health_check():
    mongodb_connected = mongo_storage.is_connected() if mongo_storage else False
    json_properties_count = len(property_manager.properties) if property_manager else 0
    mongo_properties_count = len(mongo_storage.get_all_properties()) if mongodb_connected else 0
    
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "data_sources": {
            "mongodb": {
                "connected": mongodb_connected,
                "available": mongo_storage is not None,
                "properties_stored": mongo_properties_count,
                "note": "Stores JSON properties + custom user properties"
            },
            "json_files": {
                "available": property_manager is not None,
                "properties_loaded": json_properties_count,
                "note": "Base properties from dataset"
            }
        },
        "system_mode": "hybrid",
        "primary_data_source": "mongodb" if mongodb_connected else "json_files"
    }

# Hybrid property endpoints (JSON + MongoDB)
@app.post("/properties")
async def add_property(property_data: PropertyCreate):
    """Add a new custom property to MongoDB"""
    if not mongo_storage or not mongo_storage.is_connected():
        raise HTTPException(status_code=503, detail="MongoDB not available. Cannot add custom properties.")
    
    try:
        # Convert Pydantic model to dict
        property_dict = property_data.dict()
        
        # Mark as custom property
        property_dict['source'] = 'user_custom'
        property_dict['is_custom'] = True
        
        # Generate a unique ID if not present
        if 'id' not in property_dict:
            import uuid
            property_dict['id'] = f"custom_{str(uuid.uuid4())[:8]}"
        
        success = mongo_storage.add_property(property_dict)
        if success:
            return {
                "message": "Custom property added successfully",
                "address": property_data.address,
                "id": property_dict['id'],
                "note": "Property can now be compared with JSON properties"
            }
        else:
            raise HTTPException(status_code=400, detail="Failed to add property")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding property: {str(e)}")

@app.get("/properties")
async def get_all_properties(limit: int = 50):
    """Get all properties from MongoDB (includes JSON + custom properties)"""
    # Try MongoDB first (has both JSON and custom properties)
    if mongo_storage and mongo_storage.is_connected():
        try:
            properties = mongo_storage.get_all_properties(limit)
            return {
                "properties": properties,
                "count": len(properties),
                "source": "mongodb_hybrid",
                "note": "Includes JSON properties + custom user properties"
            }
        except Exception as e:
            print(f"MongoDB error: {e}")
    
    # Fallback to JSON files only
    if property_manager:
        try:
            properties = property_manager.get_all_properties()[:limit]
            return {
                "properties": properties,
                "count": len(properties),
                "source": "json_files",
                "note": "JSON properties only (MongoDB not available)"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving properties from JSON: {str(e)}")
    
    raise HTTPException(status_code=503, detail="No property data source available")

@app.get("/properties/search")
async def search_properties(query: str = "", property_type: str = "", min_price: int = 0, max_price: int = 999999999, limit: int = 50):
    """Search properties in MongoDB (includes JSON + custom properties)"""
    # Try MongoDB first (has both JSON and custom properties)
    if mongo_storage and mongo_storage.is_connected():
        try:
            if query:
                properties = mongo_storage.search_properties(query, limit)
            elif property_type:
                properties = mongo_storage.get_properties_by_type(property_type)
            elif min_price > 0 or max_price < 999999999:
                properties = mongo_storage.get_properties_by_price_range(min_price, max_price)
            else:
                properties = mongo_storage.get_all_properties(limit)
            
            return {
                "properties": properties,
                "count": len(properties),
                "query": query,
                "source": "mongodb_hybrid",
                "filters": {
                    "property_type": property_type,
                    "min_price": min_price,
                    "max_price": max_price
                }
            }
        except Exception as e:
            print(f"MongoDB search error: {e}")
    
    # Fallback to JSON files only
    if property_manager:
        try:
            if query:
                properties = property_manager.search_properties(query)
            elif property_type:
                properties = property_manager.get_properties_by_type(property_type)
            elif min_price > 0 or max_price < 999999999:
                properties = property_manager.get_properties_by_price_range(min_price, max_price)
            else:
                properties = property_manager.get_all_properties()
            
            # Apply limit
            properties = properties[:limit]
            
            return {
                "properties": properties,
                "count": len(properties),
                "query": query,
                "source": "json_files",
                "filters": {
                    "property_type": property_type,
                    "min_price": min_price,
                    "max_price": max_price
                }
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching properties in JSON: {str(e)}")
    
    raise HTTPException(status_code=503, detail="No property data source available")

@app.get("/properties/{address}")
async def get_property(address: str):
    """Get a specific property by address from MongoDB or JSON files"""
    # Try MongoDB first (has both JSON and custom properties)
    if mongo_storage and mongo_storage.is_connected():
        try:
            property_data = mongo_storage.get_property_by_address(address)
            if property_data:
                property_data["source"] = "mongodb_hybrid"
                return property_data
        except Exception as e:
            print(f"MongoDB get property error: {e}")
    
    # Fallback to JSON files
    if property_manager:
        try:
            property_data = property_manager.get_property_by_address(address)
            if property_data:
                property_data["source"] = "json_files"
                return property_data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving property from JSON: {str(e)}")
    
    raise HTTPException(status_code=404, detail="Property not found")

@app.put("/properties/{address}")
async def update_property(address: str, updates: dict):
    """Update a property in MongoDB"""
    if not mongo_storage or not mongo_storage.is_connected():
        raise HTTPException(status_code=503, detail="MongoDB not available")
    
    try:
        success = mongo_storage.update_property(address, updates)
        if success:
            return {"message": "Property updated successfully", "address": address}
        else:
            raise HTTPException(status_code=404, detail="Property not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating property: {str(e)}")

@app.delete("/properties/{address}")
async def delete_property(address: str):
    """Delete a property from MongoDB"""
    if not mongo_storage or not mongo_storage.is_connected():
        raise HTTPException(status_code=503, detail="MongoDB not available")
    
    try:
        success = mongo_storage.delete_property(address)
        if success:
            return {"message": "Property deleted successfully", "address": address}
        else:
            raise HTTPException(status_code=404, detail="Property not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting property: {str(e)}")

@app.get("/properties/stats/summary")
async def get_property_stats():
    """Get database statistics"""
    # Try MongoDB first
    if mongo_storage and mongo_storage.is_connected():
        try:
            stats = mongo_storage.get_database_stats()
            stats["source"] = "mongodb"
            return stats
        except Exception as e:
            print(f"MongoDB stats error: {e}")
    
    # Fallback to JSON files
    if property_manager:
        try:
            stats = property_manager.get_stats()
            stats["source"] = "json_files"
            return stats
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving stats from JSON: {str(e)}")
    
    raise HTTPException(status_code=503, detail="No property data source available")

@app.get("/properties/stats/sources")
async def get_property_sources():
    """Get breakdown of property sources (JSON vs Custom)"""
    if mongo_storage and mongo_storage.is_connected():
        try:
            all_properties = mongo_storage.get_all_properties()
            json_properties = [p for p in all_properties if p.get('source') == 'json_file']
            custom_properties = [p for p in all_properties if p.get('source') == 'user_custom']
            
            return {
                "total_properties": len(all_properties),
                "json_properties": {
                    "count": len(json_properties),
                    "source": "Loaded from JSON files",
                    "editable": False
                },
                "custom_properties": {
                    "count": len(custom_properties),
                    "source": "Added by users",
                    "editable": True
                },
                "data_source": "mongodb_hybrid"
            }
        except Exception as e:
            print(f"MongoDB sources error: {e}")
    
    # Fallback to JSON files only
    if property_manager:
        json_count = len(property_manager.properties)
        return {
            "total_properties": json_count,
            "json_properties": {
                "count": json_count,
                "source": "JSON files only",
                "editable": False
            },
            "custom_properties": {
                "count": 0,
                "source": "Not available (MongoDB not connected)",
                "editable": False
            },
            "data_source": "json_files_only"
        }
    
    raise HTTPException(status_code=503, detail="No property data source available")

@app.post("/compare-properties-mongo")
async def compare_properties_from_mongo(request_data: dict):
    """Compare two properties stored in MongoDB or JSON files"""
    address1 = request_data.get("address1", "").strip()
    address2 = request_data.get("address2", "").strip()
    
    if not address1 or not address2:
        raise HTTPException(status_code=400, detail="Both address1 and address2 are required")
    
    property1_data = None
    property2_data = None
    source = "unknown"
    
    # Try MongoDB first
    if mongo_storage and mongo_storage.is_connected():
        try:
            property1_data = mongo_storage.get_property_by_address(address1)
            property2_data = mongo_storage.get_property_by_address(address2)
            if property1_data and property2_data:
                source = "mongodb"
        except Exception as e:
            print(f"MongoDB comparison error: {e}")
    
    # Fallback to JSON files
    if (not property1_data or not property2_data) and property_manager:
        try:
            if not property1_data:
                property1_data = property_manager.get_property_by_address(address1)
            if not property2_data:
                property2_data = property_manager.get_property_by_address(address2)
            
            if property1_data and property2_data:
                source = "json_files"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving properties from JSON: {str(e)}")
    
    # Check if we found both properties
    if not property1_data:
        raise HTTPException(status_code=404, detail=f"Property not found: {address1}")
    if not property2_data:
        raise HTTPException(status_code=404, detail=f"Property not found: {address2}")
    
    try:
        # Use existing market values or predict prices
        property1_price = property1_data.get("market_value", 0)
        property2_price = property2_data.get("market_value", 0)
        
        # If no market value, use ML prediction
        if not property1_price:
            ml_data1 = convert_mongo_to_ml_format(property1_data)
            property1_price = predict_price(ml_data1)
        
        if not property2_price:
            ml_data2 = convert_mongo_to_ml_format(property2_data)
            property2_price = predict_price(ml_data2)
        
        return {
            "property1": {**property1_data, "predicted_price": property1_price},
            "property2": {**property2_data, "predicted_price": property2_price},
            "price_difference": abs(property1_price - property2_price),
            "higher_priced": address1 if property1_price > property2_price else address2,
            "source": source
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing properties: {str(e)}")

def convert_mongo_to_ml_format(mongo_data: dict) -> dict:
    """Convert MongoDB property data to ML model format"""
    return {
        "property_type": mongo_data.get("property_type", "SFH"),
        "lot_area": mongo_data.get("lot_size", 0),
        "building_area": mongo_data.get("square_footage", 0),
        "bedrooms": mongo_data.get("bedrooms", 2),
        "bathrooms": mongo_data.get("bathrooms", 2),
        "year_built": mongo_data.get("year_built", 2000),
        "has_pool": "pool" in mongo_data.get("amenities", []),
        "has_garage": mongo_data.get("garage", 0) > 0,
        "school_rating": random.randint(5, 9)  # Default rating
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)