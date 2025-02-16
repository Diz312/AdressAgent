import os
from datetime import datetime
import json
import pytz
from persistance.storage_handler import StorageHandler

class JSONStorageHandler(StorageHandler):
    """
    Handles storing and retrieving address and log data using JSON files.
    """
    def __init__(self):
        self.address_file = os.environ.get('ADDRESS_FILE')
        self.log_file = os.environ.get('LOG_FILE')

    def save_addresses(self, data):
        """Appends address data to the JSON file."""
        with open(self.address_file, 'w') as f:
            f.write(json.dumps(data) + '\n')

    def save_logs(self, log_entry):
        """Appends a log entry to the JSON file."""
        with open(self.log_file, 'w') as f:
            f.write(json.dumps(log_entry) + '\n')

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
    
    # Example log entry
    log_entry = {
        "timestamp": datetime.now(pytz.utc).isoformat(),
        "agent": "Address Validation Agent",
        "message": "Validated address: 123 Main St, Springfield, IL."
    }
    
    storage.save_logs(log_entry)
