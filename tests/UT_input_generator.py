import pytest
from pytest_mock import mocker
import json
from datetime import datetime
from jsonschema import validate
import os
from agents.input_generator import InitialInputGenerationAgent
from persistance.json_storage import JSONStorageHandler

# Load JSON Schema from environment variable
schema_path = os.getenv('SCHEMA_INPUT_ADDRESS')
if schema_path is None:
    raise EnvironmentError("SCHEMA_INPUT_ADDRESS environment variable not set")

with open(schema_path, "r") as schema_file:
    address_schema = json.load(schema_file)

@pytest.fixture
def agent():
    return InitialInputGenerationAgent()

@pytest.fixture
def mock_llm_response():
    return json.dumps({
        "input_addresses": [
            {"original_address": "123 Main St, Apt 4B, New York, NY, 10001, USA"},
            {"original_address": "456 Elm St, Floor 3, New York, NY, 10002, USA"}
        ]
    })

@pytest.fixture
def mock_storage(mocker):
    mock_storage = mocker.patch.object(JSONStorageHandler, 'save_addresses')
    mock_logs = mocker.patch.object(JSONStorageHandler, 'save_logs')
    return mock_storage, mock_logs

@pytest.fixture
def mock_user_input(mocker):
    return mocker.patch('builtins.input', side_effect=["New York", "Residential", "Yes"])

@pytest.fixture
def mock_llm(mocker, mock_llm_response):
    mock_llm = mocker.patch.object(InitialInputGenerationAgent, 'llm')
    mock_llm.return_value.content = mock_llm_response
    return mock_llm

def test_agent_workflow(mock_user_input, mock_storage, mock_llm, agent):
    """
    Test the full workflow of Initial Input Generation Agent using pytest,
    ensuring the output follows the defined JSON schema.
    """
    agent.run()
    
    # Verify user input was captured
    mock_user_input.assert_called()
    
    # Verify addresses were generated and stored
    mock_storage[0].assert_called_once()
    saved_data = {"input_addresses": mock_storage[0].call_args[0][0]}
    
    # Validate output against JSON schema
    validate(instance=saved_data, schema=address_schema)
    
    # Verify logs were saved
    mock_storage[1].assert_called_once()
    log_entry = mock_storage[1].call_args[0][0]
    assert "Generated and stored" in log_entry["message"]
