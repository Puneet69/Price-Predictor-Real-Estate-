# MongoDB Setup Guide

## Option 1: Using Docker (Recommended)

### Start MongoDB with Docker Compose
```bash
# Start MongoDB service
docker-compose up mongodb -d

# Verify MongoDB is running
docker-compose logs mongodb
```

### Access MongoDB
- **Connection String**: `mongodb://admin:password@localhost:27017/property_comparison?authSource=admin`
- **Username**: admin
- **Password**: password
- **Database**: property_comparison

## Option 2: Local MongoDB Installation

### macOS (using Homebrew)
```bash
# Install MongoDB Community Edition
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
brew services start mongodb/brew/mongodb-community

# Or start manually
mongod --config /usr/local/etc/mongod.conf
```

### Ubuntu/Debian
```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod
```

### Windows
1. Download MongoDB Community Server from https://www.mongodb.com/try/download/community
2. Run the installer
3. Start MongoDB service from Services or run `mongod` command

## Option 3: MongoDB Atlas (Cloud)

### Setup Cloud Database
1. Go to https://www.mongodb.com/atlas
2. Create a free account
3. Create a new cluster
4. Get connection string
5. Update backend connection in `mongodb_storage.py`

```python
# Update connection string in mongodb_storage.py
storage = PropertyMongoStorage("mongodb+srv://username:password@cluster.mongodb.net/property_comparison")
```

## Testing MongoDB Connection

### Test with Python
```bash
cd backend
source venv/bin/activate
python mongodb_storage.py
```

### Expected Output
```
✅ Connected to MongoDB successfully
✅ Database indexes created successfully
🧪 TESTING MONGODB STORAGE
========================================

1. Testing property addition...
   Result: ✅ Success
   
2. Testing property retrieval...
   Result: ✅ Found
   
3. Testing property search...
   Found 1 properties
   
4. Testing database stats...
   Total properties: 1
   Property types: {'SFH': 1}
   
✅ MongoDB connection closed
✅ MongoDB storage test completed!
```

## API Endpoints

Once MongoDB is running, the following endpoints will be available:

### Property Management
- `POST /properties` - Add new property
- `GET /properties` - Get all properties
- `GET /properties/search` - Search properties
- `GET /properties/{address}` - Get specific property
- `PUT /properties/{address}` - Update property
- `DELETE /properties/{address}` - Delete property

### Statistics
- `GET /properties/stats/summary` - Get database statistics

### Comparison
- `POST /compare-properties-mongo` - Compare properties from MongoDB

## Frontend Features

### Property Manager Tab
- Add new properties to database
- Search and filter properties
- Select and compare properties
- View database statistics
- Real-time property management

### Compare Properties Tab
- Original property comparison using ML model
- Works with both file-based and MongoDB data

## Troubleshooting

### MongoDB Connection Issues
1. **Connection refused**: Make sure MongoDB is running
2. **Authentication failed**: Check username/password
3. **Database not found**: Database is created automatically
4. **Port conflicts**: Make sure port 27017 is available

### Backend Issues
1. **Import errors**: Install pymongo with `pip install pymongo`
2. **Module not found**: Make sure you're in the correct virtual environment
3. **API errors**: Check backend logs for detailed error messages

### Frontend Issues
1. **CORS errors**: Make sure backend CORS is configured properly
2. **API connection**: Verify backend is running on port 8000
3. **Component errors**: Check browser console for JavaScript errors

## Data Migration

### Import Existing .json.txt Files
```bash
# Run the conversion script
cd dataset
python convert_json_txt.py

# Or use the backend API to add properties programmatically
```

### Backup MongoDB Data
```bash
# Export data
mongodump --uri="mongodb://admin:password@localhost:27017/property_comparison?authSource=admin"

# Import data
mongorestore --uri="mongodb://admin:password@localhost:27017/property_comparison?authSource=admin" dump/
```

## Security Notes

### Production Setup
- Change default MongoDB credentials
- Use environment variables for connection strings
- Enable MongoDB authentication
- Use SSL/TLS for connections
- Implement proper user roles and permissions

### Development Setup
- Default credentials are fine for local development
- MongoDB runs without authentication by default in some setups
- Use Docker for consistent development environment