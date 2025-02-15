# Configuration Module

This module is designed to manage configuration settings and secrets for your application. It provides a structured way to load, process, and access configuration data and environment variables.

## Overview

The module consists of the following components:

1. **`config.json`**: A JSON file that contains configuration settings for your application. It supports variable interpolation, allowing you to reference other configuration values within the file.

2. **`load_config.py`**: A Python script that loads and processes the configuration data from `config.json`. It handles variable interpolation, path normalization, and exports configuration values as environment variables.

3. **`secrets.env`**: A file for storing sensitive information such as API keys. This file should be kept secure and not committed to version control.

## How It Works

### `config.json`

- This file contains key-value pairs for configuration settings.
- Supports variable interpolation using the `${VARIABLE_NAME}` syntax, allowing you to reference other configuration values.
- Example:
  ```json
  {
    "PYTHONPATH": "E:/Python/GitHub/AdressAgent",
    "STORAGEPATH": "${PYTHONPATH}/storage",
    "ADDRESS_FILE": "addresses.json",
    "LOG_FILE": "logs.json"
  }
  ```

### `load_config.py`

- **Purpose**: Loads and processes the configuration data from `config.json`.
- **Key Functions**:
  - `process_variable`: Recursively resolves variable references within configuration values.
  - `normalize_path`: Converts path strings to system-specific formats.
  - `load_config`: Reads `config.json`, processes variable interpolations, normalizes paths, and exports values as environment variables.
- **Usage**: The script creates a singleton `Config` instance that can be used throughout your application to access configuration values.
- **Example**:
  ```python
  from config.load_config import config

  print(config.PYTHONPATH)  # Access a configuration value
  ```

### `secrets.env`

- **Purpose**: Stores sensitive information such as API keys.
- **Example**:
  ```env
  LLM_API_KEY="your_llm_api_key_here"
  ```
- **Security**: Ensure this file is not committed to version control. Use a `.gitignore` file to exclude it.

## Best Practices

- **Environment Variables**: Use environment variables for sensitive information and configuration settings that may change between environments (development, testing, production).
- **Variable Interpolation**: Leverage the variable interpolation feature in `config.json` to avoid duplication and simplify configuration management.
- **Path Normalization**: Use the path normalization feature to ensure paths are correctly formatted across different operating systems.

## Example Usage

Here's how you can use the configuration module in your application:
