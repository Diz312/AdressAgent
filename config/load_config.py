import json
import os
from typing import Any
from pathlib import Path

class Config:
    def __init__(self, config_data: dict[str, Any]):
        self._config = config_data
        
        # Set all config values as attributes
        for key, value in self._config.items():
            setattr(self, key, value)
    
    def __getitem__(self, key: str) -> Any:
        return self._config[key]
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)

def process_variable(value: str, config_data: dict[str, Any], processed: set[str] = None) -> str:
    """
    Recursively process variables in a string, handling nested references
    """
    if not isinstance(value, str) or '${' not in value:
        return value

    if processed is None:
        processed = set()

    # Prevent infinite recursion
    if value in processed:
        raise ValueError(f"Circular reference detected in config: {value}")
    
    processed.add(value)
    
    for var_key in config_data:
        placeholder = f'${{{var_key}}}'
        if placeholder in value:
            replacement = str(config_data[var_key])
            # Recursively process the replacement value
            replacement = process_variable(replacement, config_data, processed)
            value = value.replace(placeholder, replacement)
    
    return value

def normalize_path(path_str: str) -> str:
    """
    Convert path string to system-specific format
    """
    # Convert forward/backward slashes to system-specific separator
    path = Path(path_str)
    return str(path.absolute() if path.is_absolute() else path)

def load_env_file(env_path: Path) -> dict[str, str]:
    """
    Load environment variables from a .env file
    """
    env_data = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_data[key.strip()] = value.strip()
    return env_data

def load_config() -> Config:
    # Read the config file
    config_path = Path(__file__).parent / 'config.json'
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    
    # Read the secrets.env file
    env_path = Path(__file__).parent / 'secrets.env'
    env_data = load_env_file(env_path)
    
    # Merge config data with env data
    combined_data = {**config_data, **env_data}
    
    # First pass: Process all variable interpolations
    processed_config = {}
    for key, value in combined_data.items():
        processed_value = process_variable(value, combined_data)
        processed_config[key] = processed_value
    
    # Second pass: Normalize all paths (automatically detect path keys)
    path_keys = [key for key in processed_config.keys() if key.endswith('_PATH')]
    for key in path_keys:
        processed_config[key] = normalize_path(processed_config[key])
    
    # Export all config values to environment variables
    for key, value in processed_config.items():
        os.environ[key] = str(value)
    
    return Config(processed_config)

# Create a singleton instance
config = load_config()

# Usage example in __main__
if __name__ == '__main__':
    def pretty_print_env_vars(indent=0):
        """Recursively print environment variables with proper indentation"""
        for key, value in os.environ.items():
            prefix = "    " * indent
            print(f"{prefix}{key}: {value}")

    print("Environment variables:")
    pretty_print_env_vars()
    
    # Test nested variable resolution
    # If you had something like:
    # {
    #   "BASE_DIR": "E:/Python/GitHub/AdressAgent",
    #   "DATA_DIR": "${BASE_DIR}/data",
    #   "CACHE_PATH": "${DATA_DIR}/cache"
    # }
    # It would resolve correctly 