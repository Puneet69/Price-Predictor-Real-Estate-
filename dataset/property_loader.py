"""
Property Dataset Loader
Handles loading and searching property data from JSON files
"""

import json
import os
import re
from typing import Dict, Any, Optional, List
from difflib import SequenceMatcher

class PropertyDatasetLoader:
    def __init__(self, dataset_path: str = "dataset"):
        self.dataset_path = dataset_path
        self.properties_path = os.path.join(dataset_path, "properties")
        self.index_file = os.path.join(dataset_path, "property_index.json")
        self.index_data = self.load_index()
        
        # Auto-scan for new .json.txt files and update index
        self.scan_and_update_index()
    
    def load_index(self) -> Dict[str, Any]:
        """Load the property index file"""
        try:
            with open(self.index_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Property index file not found at {self.index_file}")
            return {"properties": [], "search_patterns": []}
    
    def normalize_address(self, address: str) -> str:
        """Normalize address for better matching"""
        # Convert to lowercase and remove extra spaces
        normalized = re.sub(r'\s+', ' ', address.lower().strip())
        
        # Common abbreviations
        abbreviations = {
            ' street': ' st',
            ' avenue': ' ave', 
            ' road': ' rd',
            ' drive': ' dr',
            ' boulevard': ' blvd',
            ' lane': ' ln',
            ' court': ' ct'
        }
        
        for full, abbrev in abbreviations.items():
            normalized = normalized.replace(full, abbrev)
            normalized = normalized.replace(abbrev, abbrev)  # Ensure consistency
            
        return normalized
    
    def find_property_by_address(self, address: str) -> Optional[str]:
        """Find property file by address using fuzzy matching"""
        normalized_input = self.normalize_address(address)
        best_match = None
        best_score = 0.0
        
        for prop in self.index_data.get("properties", []):
            prop_address = self.normalize_address(prop["address"])
            
            # Calculate similarity score
            score = SequenceMatcher(None, normalized_input, prop_address).ratio()
            
            if score > best_score and score > 0.7:  # 70% similarity threshold
                best_score = score
                best_match = prop["file"]
        
        # Also check search patterns for exact matches
        for pattern in self.index_data.get("search_patterns", []):
            pattern_normalized = self.normalize_address(pattern)
            if pattern_normalized == normalized_input:
                # Find corresponding property file
                for prop in self.index_data.get("properties", []):
                    if self.normalize_address(prop["address"]) == pattern_normalized:
                        return prop["file"]
        
        return best_match
    
    def load_property_data(self, address: str) -> Optional[Dict[str, Any]]:
        """Load property data from JSON file by address"""
        property_file = self.find_property_by_address(address)
        
        if not property_file:
            return None
        
        file_path = os.path.join(self.properties_path, property_file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ Loaded real property data for: {address}")
                return data
        except FileNotFoundError:
            print(f"Warning: Property file not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing property file {file_path}: {e}")
            return None
    
    def get_all_properties(self) -> List[Dict[str, Any]]:
        """Load all properties from the dataset"""
        properties = []
        
        for prop in self.index_data.get("properties", []):
            file_path = os.path.join(self.properties_path, prop["file"])
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    properties.append(data)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading {prop['file']}: {e}")
        
        return properties
    
    def add_property(self, property_data: Dict[str, Any]) -> bool:
        """Add a new property to the dataset"""
        try:
            # Generate filename from address
            address = property_data.get("address", "")
            filename = re.sub(r'[^\w\s-]', '', address.lower()).replace(' ', '_') + '.json'
            
            # Save property file
            file_path = os.path.join(self.properties_path, filename)
            with open(file_path, 'w') as f:
                json.dump(property_data, f, indent=2)
            
            # Update index
            new_entry = {
                "id": f"custom_{len(self.index_data.get('properties', []))}",
                "address": property_data.get("address"),
                "file": filename,
                "property_type": property_data.get("property_type"),
                "city": property_data.get("city"),
                "state": property_data.get("state"),
                "market_value": property_data.get("market_value", 0)
            }
            
            self.index_data.setdefault("properties", []).append(new_entry)
            self.index_data["dataset_info"]["total_properties"] = len(self.index_data["properties"])
            
            # Save updated index
            with open(self.index_file, 'w') as f:
                json.dump(self.index_data, f, indent=2)
            
            print(f"✅ Added new property: {property_data.get('address')}")
            return True
            
        except Exception as e:
            print(f"Error adding property: {e}")
            return False
    
    def scan_and_update_index(self):
        """Scan for .json and .json.txt files and update the index"""
        if not os.path.exists(self.properties_path):
            print(f"Properties directory not found: {self.properties_path}")
            return
        
        existing_files = set()
        for prop in self.index_data.get("properties", []):
            existing_files.add(prop["file"])
        
        # Scan for property files
        new_files_added = False
        for filename in os.listdir(self.properties_path):
            if filename.endswith(('.json', '.json.txt')) and filename not in existing_files:
                file_path = os.path.join(self.properties_path, filename)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    
                    # Add to index
                    new_entry = {
                        "id": f"auto_{len(self.index_data.get('properties', []))}",
                        "address": data.get("address", "Unknown Address"),
                        "file": filename,
                        "property_type": data.get("property_type", "Unknown"),
                        "city": data.get("city", "Unknown"),
                        "state": data.get("state", "Unknown"),
                        "market_value": data.get("market_value", 0)
                    }
                    
                    self.index_data.setdefault("properties", []).append(new_entry)
                    new_files_added = True
                    print(f"🆕 Auto-added to index: {filename} - {data.get('address', 'Unknown')}")
                    
                except (json.JSONDecodeError, FileNotFoundError) as e:
                    print(f"⚠️  Skipped invalid file {filename}: {e}")
        
        if new_files_added:
            # Update dataset info
            self.index_data["dataset_info"]["total_properties"] = len(self.index_data["properties"])
            
            # Save updated index
            try:
                with open(self.index_file, 'w') as f:
                    json.dump(self.index_data, f, indent=2)
                print(f"✅ Updated property index with {len(self.index_data['properties'])} total properties")
            except Exception as e:
                print(f"Error updating index: {e}")

    def search_properties(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search properties by criteria"""
        all_properties = self.get_all_properties()
        results = []
        
        for prop in all_properties:
            match = True
            
            # Check each criteria
            for key, value in criteria.items():
                if key in prop:
                    if isinstance(value, str):
                        if value.lower() not in str(prop[key]).lower():
                            match = False
                            break
                    elif prop[key] != value:
                        match = False
                        break
            
            if match:
                results.append(prop)
        
        return results

# Example usage and testing
if __name__ == "__main__":
    loader = PropertyDatasetLoader()
    
    # Test loading properties
    test_addresses = [
        "123 Main Street, San Francisco, CA",
        "456 Oak Avenue, Los Angeles, CA",
        "789 Pine Road, Seattle, WA",
        "321 Elm Street, New York, NY"
    ]
    
    for address in test_addresses:
        data = loader.load_property_data(address)
        if data:
            print(f"Found: {data['address']} - ${data['market_value']:,}")
        else:
            print(f"Not found: {address}")