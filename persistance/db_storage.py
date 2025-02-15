from persistance.storage_handler import StorageHandler

class DatabaseStorageHandler(StorageHandler):
    """
    Placeholder for future database integration.
    This class will implement the StorageHandler interface using a database backend.
    """
    def __init__(self):
        raise NotImplementedError("Database storage is not yet implemented")

    def save_addresses(self, data):
        """Save address data to database."""
        raise NotImplementedError("Database storage is not yet implemented")

    def load_addresses(self):
        """Load address data from database."""
        raise NotImplementedError("Database storage is not yet implemented")

    def save_logs(self, log_entry):
        """Save a log entry to database."""
        raise NotImplementedError("Database storage is not yet implemented")

    def load_logs(self):
        """Load logs from database."""
        raise NotImplementedError("Database storage is not yet implemented") 