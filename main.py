import os
from config.load_config import config
from persistance.json_storage import JSONStorageHandler

def main():
    # Call the function or create an instance of the class
    result = JSONStorageHandler()
    print(result)
    
    print(os.getenv('ADDRESS_FILE'))
    print(os.getenv('LOG_FILE'))  
    print(os.getenv('STORAGEPATH'))
    print(os.getenv('PYTHONPATH'))

if __name__ == "__main__":
    main()
