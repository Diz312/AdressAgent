from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
import json
from datetime import datetime
import pytz
import os
import jsonschema
import yaml
from persistance.json_storage import JSONStorageHandler
from config.load_config import config

class InitialInputGenerationAgent:
    """
    Agent responsible for interacting with the user to generate an initial set of raw addresses.
    """
    def __init__(self, model_name='gpt-4o', temperature=0.5):
        open_api_key = os.getenv('OPEN_API_KEY')  # Retrieve the API key from environment variables
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature, api_key=open_api_key)
        self.memory = ConversationBufferMemory()
        self.storage = JSONStorageHandler()
        with open('./agents/prompts.yaml', 'r') as file:
            self.prompts = yaml.safe_load(file)

    def ask_user_questions(self):
        """
        Ask user 2-3 questions to infer address details.
        """
        questions = [
            "Which city or region should the addresses be from?",
            "Do you need residential, commercial, or mixed-type addresses?",
            "Should we include apartment buildings and units? (Yes/No)"
        ]
        
        responses = {}
        for question in questions:
            response = input(f"{question} ")
            responses[question] = response
            
        return responses
    
    def generate_addresses(self, user_responses):
        """
        Uses LLM to generate synthetic address data based on user responses.
        """
        # Load the JSON schema
        schema_path = os.getenv('SCHEMA_INPUT_ADDRESS')  # Retrieve the schema path from environment variables
        with open(schema_path) as schema_file:
            schema = json.load(schema_file)

        # Load the prompt from the YAML file
        prompt_template = self.prompts['PROMPT_INPUT_GENERATOR']
        prompt = prompt_template.replace("{{schema}}", json.dumps(schema, indent=4))
        prompt = prompt.replace("{{city_region}}", user_responses['Which city or region should the addresses be from?'])
        prompt = prompt.replace("{{address_type}}", user_responses['Do you need residential, commercial, or mixed-type addresses?'])
        prompt = prompt.replace("{{include_apartments}}", user_responses['Should we include apartment buildings and units? (Yes/No)'])

        response = self.llm.invoke(prompt)
        print(response)
        try:
            response_json = json.loads(response.content)
            jsonschema.validate(instance=response_json, schema=schema)
            return response_json.get("input_addresses", [])
        except (json.JSONDecodeError, jsonschema.exceptions.ValidationError) as e:
            log_entry = {
                "timestamp": datetime.now(pytz.utc).isoformat(),
                "agent": "Initial Input Generation Agent",
                "message": f"Error: LLM did not provide a proper JSON response. {e}"
            }
            self.storage.save_logs(log_entry)
            return []  # Return empty list if invalid
  
    def save_generated_addresses(self, addresses):
        """
        Saves the generated addresses to the JSON storage system.
        """
        formatted_addresses = {"input_addresses": addresses}
        self.storage.save_addresses(formatted_addresses)
        
        # Log the event
        log_entry = {
            "timestamp": datetime.now(pytz.utc).isoformat(),
            "agent": "Initial Input Generation Agent",
            "message": f"Generated and stored {len(formatted_addresses['input_addresses'])} addresses."
        }
        self.storage.save_logs(log_entry)
    
    def run(self):
        """
        Executes the agent workflow: asks user questions, generates addresses, and stores them.
        """
        user_responses = self.ask_user_questions()
        addresses = self.generate_addresses(user_responses)
        self.save_generated_addresses(addresses)
        print("Addresses successfully generated and stored!")
        
# Example usage
if __name__ == "__main__":
    agent = InitialInputGenerationAgent()
    agent.run()
