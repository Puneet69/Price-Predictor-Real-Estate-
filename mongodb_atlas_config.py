# MongoDB Atlas Configuration for Property Comparison App

# Your MongoDB Atlas Details:
MONGODB_CLUSTER = "realestate.caqfzde.mongodb.net"
MONGODB_USERNAME = "price_predictor"
MONGODB_PASSWORD = "vlMUA2FIr48bnJWO"
MONGODB_APP_NAME = "RealEstate"

# Complete Connection String:
MONGODB_URI = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_CLUSTER}/property_comparison?retryWrites=true&w=majority&appName={MONGODB_APP_NAME}"

# Full Connection String (ready to use):
# mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate

print("✅ MongoDB Atlas connection string configured!")
print(f"🔗 Connection: {MONGODB_URI}")