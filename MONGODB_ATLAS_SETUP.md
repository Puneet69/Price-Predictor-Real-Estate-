# 🏗️ MongoDB Atlas Setup & Configuration Guide

## 📋 **Your MongoDB Atlas Details**

### **Connection Information:**
- **Cluster**: `realestate.caqfzde.mongodb.net`
- **Username**: `price_predictor`
- **Password**: `vlMUA2FIr48bnJWO`
- **Database**: `property_comparison`
- **App Name**: `RealEstate`

### **Complete Connection String:**
```
mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate
```

## 🔧 **Local Development Setup**

### **1. Environment Configuration**
Your `.env` file is already configured with:
```bash
MONGODB_URI=mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate
DATABASE_NAME=property_comparison
NODE_ENV=production
```

### **2. Backend Integration**
Your `backend/main.py` is already configured to:
- ✅ Use `MONGODB_URI` environment variable
- ✅ Fallback to Atlas connection if env var not set
- ✅ Support hybrid JSON + MongoDB system
- ✅ Sync JSON properties to MongoDB on startup

### **3. Test Your Connection**
Run the connection test:
```bash
cd "/Users/puneet/Desktop/Case Study 2"
python test_mongodb_atlas.py
```

Expected output:
```
🧪 TESTING MONGODB ATLAS CONNECTION
✅ Successfully connected to MongoDB Atlas!
✅ Your MongoDB Atlas connection is working perfectly!
```

## 🚀 **Production Deployment Configuration**

### **For Railway:**
Set environment variable in Railway dashboard:
```
MONGODB_URI=mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate
```

### **For Render:**
Add to environment variables:
```
MONGODB_URI=mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate
```

### **For DigitalOcean:**
Update `.do/app.yaml`:
```yaml
envs:
- key: MONGODB_URI
  value: "mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate"
```

## 📊 **Database Structure**

### **Collections:**
- **`properties`** - Main property data collection
  - JSON properties (synced from dataset files)
  - Custom user properties
  - Both use same schema

### **Document Schema:**
```javascript
{
  "_id": ObjectId("..."),
  "address": "123 Main St, City, State 12345",
  "property_type": "SFH",
  "lot_size": 5000,
  "square_footage": 2200,
  "bedrooms": 3,
  "bathrooms": 2,
  "garage": 2,
  "year_built": 2015,
  "market_value": 750000,
  "amenities": ["pool", "garage"],
  "condition": "excellent",
  "source": "json_file" | "user_custom",
  "is_custom": false | true,
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}
```

## 🔒 **Security Best Practices**

### **1. IP Whitelist Configuration**
In MongoDB Atlas:
- Go to Network Access
- Add your deployment platform's IP ranges:
  - **Railway**: Add `0.0.0.0/0` (all IPs) for dynamic IPs
  - **Render**: Add `0.0.0.0/0` for simplicity
  - **DigitalOcean**: Add specific IP ranges if available

### **2. User Permissions**
Your `price_predictor` user should have:
- ✅ Read/Write access to `property_comparison` database
- ✅ Index creation permissions
- ❌ No admin privileges (security)

### **3. Connection Security**
- ✅ Using SSL/TLS encryption (mongodb+srv://)
- ✅ Connection string includes retry logic
- ✅ App name specified for monitoring

## 🛠️ **Using Multiple Projects with Same Database**

### **Database-Level Separation (Recommended):**
```python
# Project 1: Use database "property_comparison"
MONGODB_URI_PROJECT1 = "mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?..."

# Project 2: Use database "project2_database"  
MONGODB_URI_PROJECT2 = "mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/project2_database?..."
```

### **Collection-Level Separation:**
```python
# Same database, different collections
# Project 1: Use collections "properties", "users", etc.
# Project 2: Use collections "project2_properties", "project2_users", etc.
```

## 📈 **Monitoring & Maintenance**

### **1. Atlas Dashboard Monitoring**
- Monitor connection count
- Check query performance
- Review storage usage

### **2. Application Logging**
Your app logs:
- ✅ Connection status
- ✅ Property operations
- ✅ Sync operations
- ✅ Error details

### **3. Backup Strategy**
MongoDB Atlas automatically:
- ✅ Creates continuous backups
- ✅ Provides point-in-time recovery
- ✅ Retains backups per tier settings

## 🚨 **Troubleshooting Common Issues**

### **Connection Timeouts:**
```python
# Add connection timeout parameters
mongodb+srv://price_predictor:vlMUA2FIr48bnJWO@realestate.caqfzde.mongodb.net/property_comparison?retryWrites=true&w=majority&appName=RealEstate&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000
```

### **Authentication Errors:**
1. Verify username: `price_predictor`
2. Verify password: `vlMUA2FIr48bnJWO`
3. Check user permissions in Atlas dashboard

### **Network Issues:**
1. Check IP whitelist in Atlas
2. Verify internet connectivity
3. Test connection from deployment platform

## ✅ **Verification Checklist**

- [ ] MongoDB Atlas cluster is running
- [ ] IP address whitelisted (0.0.0.0/0 for production)
- [ ] User `price_predictor` has correct permissions
- [ ] Environment variable `MONGODB_URI` set in deployment
- [ ] Test connection script passes locally
- [ ] App can sync JSON properties to MongoDB
- [ ] Custom properties can be added/retrieved

## 🎯 **Ready for Production!**

Your Property Comparison App is now configured to use MongoDB Atlas in production. The hybrid system will:

1. **Sync JSON properties** to MongoDB on startup
2. **Store custom properties** in MongoDB
3. **Provide unified API** for all property operations
4. **Scale automatically** with MongoDB Atlas
5. **Work across multiple deployment platforms**

---

**Next Step**: Deploy your app and verify the MongoDB Atlas connection in production! 🚀