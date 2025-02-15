import sys
import os
from datetime import datetime
import json
import pytz

# Add the root directory of the project to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.load_config import config
from persistance.storage_handler import StorageHandler


class JSONStorageHandler(StorageHandler):
    """
    Handles storing and retrieving address and log data using JSON files.
    """
    def __init__(self):
        self.address_file = os.environ.get('ADDRESS_FILE')
        self.log_file = os.environ.get('LOG_FILE')
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Ensures the required JSON files exist."""
        if not os.path.exists(self.address_file):
            with open(self.address_file, 'w') as f:
                json.dump({"addresses": []}, f)

        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump({"logs": []}, f)

    def save_addresses(self, data):
        """Saves address data to the JSON file."""
        with open(self.address_file, 'w') as f:
            json.dump({"addresses": data}, f, indent=4)

    def load_addresses(self):
        """Loads address data from the JSON file."""
        with open(self.address_file, 'r') as f:
            return json.load(f).get("addresses", [])

    def save_logs(self, log_entry):
        """Appends a log entry to the JSON file."""
        logs = self.load_logs()
        logs.append(log_entry)
        with open(self.log_file, 'w') as f:
            json.dump({"logs": logs}, f, indent=4)

    def load_logs(self):
        """Loads logs from the JSON file."""
        with open(self.log_file, 'r') as f:
            return json.load(f).get("logs", []) 
        
# Example usage
if __name__ == "__main__":
    # The config import above ensures that environment variables are set
    storage = JSONStorageHandler()
    
    # Example address data following the comprehensive schema
    sample_address = {
        "original_address": "123 Main St, Apt 4B, Springfield, IL, 62704, USA",
        "cleansed_address": {
            "house_number": "123",
            "street_name": "Main",
            "street_suffix": "St",
            "unit_number": "4B",
            "floor_number": "",
            "building_name": "",
            "neighborhood": "",
            "city": "Springfield",
            "state": "IL",
            "postal_code": "62704",
            "country": "USA"
        },
        "validated": True,
        "latitude": 39.7817,
        "longitude": -89.6501,
        "error_message": ""
    }
    
    storage.save_addresses([sample_address])
    print(storage.load_addresses())
    
    # Example log entry
    log_entry = {
        "timestamp": datetime.now(pytz.utc).isoformat(),
        "agent": "Address Validation Agent",
        "message": "Validated address: 123 Main St, Springfield, IL."
    }
    
    storage.save_logs(log_entry)
    print(storage.load_logs())
