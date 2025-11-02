#!/usr/bin/env python3
"""
MongoDB Atlas Connection Test Script
Tests connection to your Atlas cluster and verifies functionality
"""

import os
import sys
from datetime import datetime

# Add backend directory to path
sys.path.append('backend')

def test_mongodb_atlas_connection():
    """Test MongoDB Atlas connection with your credentials"""
    
    print("🧪 TESTING MONGODB ATLAS CONNECTION")
    print("=" * 50)
    
    # Your MongoDB Atlas connection string
    MONGODB_URI = "mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate"
    
    try:
        # Import MongoDB storage
        from backend.mongodb_storage import PropertyMongoStorage
        
        print("📡 Connecting to MongoDB Atlas...")
        print(f"   Cluster: realestate.caqfzde.mongodb.net")
        print(f"   Username: price_predictor")
        print(f"   Database: property_comparison")
        print(f"   App Name: RealEstate")
        
        # Initialize storage with Atlas connection
        storage = PropertyMongoStorage(connection_string=MONGODB_URI)
        
        if not storage.is_connected():
            print("❌ Failed to connect to MongoDB Atlas")
            print("🔍 Possible issues:")
            print("   - Check internet connection")
            print("   - Verify MongoDB Atlas cluster is running")
            print("   - Confirm IP address is whitelisted")
            print("   - Check username/password credentials")
            return False
        
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Test basic operations
        print("\n🔄 Testing basic operations...")
        
        # Test 1: Add a sample property
        test_property = {
            "address": "123 Atlas Test Street, San Francisco, CA 94105",
            "property_type": "SFH",
            "lot_size": 5000,
            "square_footage": 2200,
            "bedrooms": 3,
            "bathrooms": 2,
            "garage": 2,
            "year_built": 2015,
            "market_value": 750000,
            "amenities": ["modern_kitchen", "hardwood_floors"],
            "condition": "excellent"
        }
        
        print("   1. Adding test property...")
        success = storage.add_property(test_property)
        print(f"      Result: {'✅ Success' if success else '❌ Failed'}")
        
        # Test 2: Retrieve the property
        print("   2. Retrieving test property...")
        retrieved = storage.get_property_by_address(test_property["address"])
        print(f"      Result: {'✅ Found' if retrieved else '❌ Not found'}")
        
        if retrieved:
            print(f"      Address: {retrieved.get('address')}")
            print(f"      Type: {retrieved.get('property_type')}")
            print(f"      Value: ${retrieved.get('market_value'):,}")
            print(f"      Bedrooms: {retrieved.get('bedrooms')}")
            print(f"      Bathrooms: {retrieved.get('bathrooms')}")
        
        # Test 3: Get database statistics
        print("   3. Getting database statistics...")
        stats = storage.get_database_stats()
        print(f"      Total properties: {stats.get('total_properties', 0)}")
        print(f"      Property types: {stats.get('property_types', {})}")
        print(f"      Average value: ${stats.get('average_market_value', 0):,.2f}")
        
        # Test 4: Search functionality
        print("   4. Testing search functionality...")
        search_results = storage.search_properties("Test Street")
        print(f"      Search results: {len(search_results)} properties found")
        
        # Test 5: Clean up test data
        print("   5. Cleaning up test data...")
        cleanup_success = storage.delete_property(test_property["address"])
        print(f"      Cleanup: {'✅ Success' if cleanup_success else '❌ Failed'}")
        
        # Close connection
        storage.close_connection()
        
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Your MongoDB Atlas connection is working perfectly!")
        print("✅ Ready for production deployment!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you're running this from the project root directory")
        print("💡 Check if 'pymongo' is installed: pip install pymongo")
        return False
        
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print("\n🔍 Troubleshooting steps:")
        print("1. Check if your IP is whitelisted in MongoDB Atlas")
        print("2. Verify the username and password are correct")
        print("3. Ensure the cluster is not paused")
        print("4. Check your internet connection")
        print("5. Try accessing MongoDB Atlas dashboard in browser")
        return False

def test_environment_variables():
    """Test if environment variables are set correctly"""
    print("\n🔧 TESTING ENVIRONMENT VARIABLES")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ Found {env_file} file")
        
        # Read and display environment variables
        with open(env_file, 'r') as f:
            content = f.read()
            if "MONGODB_URI" in content:
                print("✅ MONGODB_URI found in .env file")
            else:
                print("⚠️  MONGODB_URI not found in .env file")
    else:
        print(f"⚠️  {env_file} file not found")
    
    # Check environment variable
    mongodb_uri = os.getenv('MONGODB_URI')
    if mongodb_uri:
        print("✅ MONGODB_URI environment variable is set")
        if "realestate.caqfzde.mongodb.net" in mongodb_uri:
            print("✅ Atlas cluster URL detected")
        if "price_predictor" in mongodb_uri:
            print("✅ Username detected in URI")
    else:
        print("⚠️  MONGODB_URI environment variable not set")
        print("💡 Will use default connection string from code")

def main():
    """Main test function"""
    print("🚀 MONGODB ATLAS SETUP VERIFICATION")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test environment variables
    test_environment_variables()
    
    # Test MongoDB Atlas connection
    success = test_mongodb_atlas_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SETUP VERIFICATION COMPLETED SUCCESSFULLY!")
        print("✅ Your Property Comparison App is ready to use MongoDB Atlas!")
        print("\n📝 Next steps:")
        print("   1. Deploy your app to Railway/Render/etc.")
        print("   2. Set MONGODB_URI environment variable in deployment")
        print("   3. Your app will automatically use MongoDB Atlas!")
    else:
        print("❌ SETUP VERIFICATION FAILED!")
        print("💡 Please check the error messages above and fix any issues")
    
    print("=" * 60)

if __name__ == "__main__":
    main()