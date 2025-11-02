#!/usr/bin/env python3
"""
Property File Converter
Converts .json.txt files to .json and adds them to the dataset
"""

import os
import json
import shutil
from property_loader import PropertyDatasetLoader

def find_json_txt_files(search_path: str):
    """Find all .json.txt files in the given path"""
    json_txt_files = []
    
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file.endswith('.json.txt'):
                json_txt_files.append(os.path.join(root, file))
    
    return json_txt_files

def convert_and_add_files(dataset_path: str = ".", search_path: str = ".."):
    """Convert .json.txt files to .json and add to dataset"""
    
    properties_dir = os.path.join(dataset_path, "properties")
    
    # Find all .json.txt files
    json_txt_files = find_json_txt_files(search_path)
    
    if not json_txt_files:
        print("🔍 No .json.txt files found in the search path")
        return
    
    print(f"📁 Found {len(json_txt_files)} .json.txt files:")
    for file in json_txt_files:
        print(f"  📄 {file}")
    
    print("\n🔄 Processing files...")
    
    converted_count = 0
    for json_txt_file in json_txt_files:
        try:
            # Read the .json.txt file
            with open(json_txt_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate required fields
            required_fields = ['address', 'property_type']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"⚠️  Skipping {json_txt_file}: Missing required fields: {missing_fields}")
                continue
            
            # Generate new filename
            address = data.get('address', 'unknown')
            clean_name = ''.join(c if c.isalnum() or c in ' -_' else '' for c in address.lower())
            clean_name = '_'.join(clean_name.split())
            new_filename = f"{clean_name}.json"
            
            # Copy to properties directory
            new_filepath = os.path.join(properties_dir, new_filename)
            
            # Check if file already exists
            if os.path.exists(new_filepath):
                print(f"⚠️  File already exists: {new_filename}, skipping...")
                continue
            
            # Save as .json file
            with open(new_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Converted: {os.path.basename(json_txt_file)} → {new_filename}")
            print(f"   Address: {data.get('address', 'Unknown')}")
            converted_count += 1
            
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in {json_txt_file}: {e}")
        except Exception as e:
            print(f"❌ Error processing {json_txt_file}: {e}")
    
    if converted_count > 0:
        print(f"\n🎉 Successfully converted {converted_count} files!")
        print("🔄 Reloading dataset to update index...")
        
        # Reload dataset to update index
        loader = PropertyDatasetLoader(dataset_path)
        print(f"📊 Dataset now contains {len(loader.index_data.get('properties', []))} properties")
        
        # Show all properties
        print("\n🏠 All properties in dataset:")
        for prop in loader.index_data.get('properties', []):
            print(f"  📍 {prop.get('address', 'Unknown')} ({prop.get('property_type', 'Unknown')})")
    else:
        print("\n💭 No files were converted")

if __name__ == "__main__":
    print("🏠 PROPERTY FILE CONVERTER")
    print("=" * 40)
    
    # Convert files
    convert_and_add_files()
    
    print("\n✨ Done! Your .json.txt files have been processed.")
    print("🚀 Restart the backend to use the new property data.")