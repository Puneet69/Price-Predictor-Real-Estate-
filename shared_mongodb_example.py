# Multi-Project MongoDB Configuration Example

# Shared MongoDB Configuration
SHARED_MONGODB_SETTINGS = {
    "connection_string": "mongodb+srv://user:pass@cluster.mongodb.net/",
    "database_name": "shared_real_estate_platform"
}

# Project-specific collection names
PROJECT_COLLECTIONS = {
    "property_comparison": {
        "properties": "comparison_properties",
        "users": "comparison_users",
        "analytics": "comparison_analytics"
    },
    "property_analytics": {
        "properties": "analytics_properties", 
        "reports": "analytics_reports",
        "users": "analytics_users"
    },
    "property_management": {
        "properties": "management_properties",
        "tenants": "management_tenants",
        "leases": "management_leases"
    }
}

# Usage Example:
class SharedMongoStorage:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.connection_string = SHARED_MONGODB_SETTINGS["connection_string"]
        self.database_name = SHARED_MONGODB_SETTINGS["database_name"]
        self.collections = PROJECT_COLLECTIONS[project_name]
        
    def get_collection(self, collection_type: str):
        collection_name = self.collections[collection_type]
        return self.db[collection_name]

# Project 1 Usage:
storage1 = SharedMongoStorage("property_comparison")
properties_collection = storage1.get_collection("properties")

# Project 2 Usage:
storage2 = SharedMongoStorage("property_analytics") 
reports_collection = storage2.get_collection("reports")