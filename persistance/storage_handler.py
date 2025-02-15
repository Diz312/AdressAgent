from abc import ABC, abstractmethod

class StorageHandler(ABC):
    """
    Abstract storage handler interface.
    This allows us to swap out JSON storage for a database later without modifying agent logic.
    """
    @abstractmethod
    def save_addresses(self, data):
        """Save address data to storage."""
        pass

    @abstractmethod
    def load_addresses(self):
        """Load address data from storage."""
        pass

    @abstractmethod
    def save_logs(self, log_entry):
        """Save a log entry to storage."""
        pass

    @abstractmethod
    def load_logs(self):    
        """Load logs from storage."""
        pass 