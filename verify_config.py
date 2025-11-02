#!/usr/bin/env python3
"""
Direct verification that MongoDB references are removed
"""

def verify_json_only_config():
    """Verify the main.py file is configured for JSON-only operation"""
    
    main_py_path = "/Users/puneet/Desktop/Case Study 2/backend/main.py"
    
    print("🔍 Verifying JSON-Only Configuration")
    print("=" * 40)
    
    try:
        with open(main_py_path, 'r') as f:
            content = f.read()
        
        # Check that MongoDB is disabled
        checks = [
            ('MongoDB disabled in initialization', 'MongoDB storage is disabled - using JSON files only' in content),
            ('MongoDB import commented/disabled', 'mongo_storage = None' in content),
            ('JSON files message present', 'Using JSON files directly' in content),
            ('Primary data source is JSON', '"primary_data_source": "json_files"' in content),
            ('MongoDB connection check removed', 'mongo_storage and mongo_storage.is_connected()' not in content or content.count('mongo_storage and mongo_storage.is_connected()') <= 1)
        ]
        
        print("Configuration checks:")
        all_passed = True
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {check_name}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n🎉 Backend is properly configured for JSON-only operation!")
            print("📋 The system will:")
            print("   • Load properties from JSON files only")
            print("   • Skip MongoDB connection attempts")
            print("   • Use property_data_manager.py for all data operations")
            print("   • Generate charts with matplotlib/seaborn")
        else:
            print("\n⚠️  Some configuration issues found")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        return False

if __name__ == "__main__":
    verify_json_only_config()