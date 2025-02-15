from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
import json
from datetime import datetime

# Add the root directory of the project to the system path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from persistance.json_storage import JSONStorageHandler

class InitialInputGenerationAgent:
    """
    Agent responsible for interacting with the user to generate an initial set of raw addresses.
    """
    def __init__(self, model_name='gpt-4', temperature=0.5):
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        self.memory = ConversationBufferMemory()
        self.storage = JSONStorageHandler()

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
        prompt = (
            f"Generate a list of 5 raw addresses based on the following user inputs:\n"
            f"City/Region: {user_responses['Which city or region should the addresses be from?']}\n"
            f"Address Type: {user_responses['Do you need residential, commercial, or mixed-type addresses?']}\n"
            f"Include Apartment Units: {user_responses['Should we include apartment buildings and units? (Yes/No)']}\n"
            f"Provide output as a JSON list of addresses."
        )
        
        response = self.llm(prompt)
        addresses = json.loads(response.content)  # Ensure LLM returns valid JSON
        
        return addresses
    
    def save_generated_addresses(self, addresses):
        """
        Saves the generated addresses to the JSON storage system.
        """
        formatted_addresses = [
            {"original_address": addr, "cleansed_address": {}, "validated": False, "latitude": None, "longitude": None, "error_message": ""}
            for addr in addresses
        ]
        
        self.storage.save_addresses(formatted_addresses)
        
        # Log the event
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": "Initial Input Generation Agent",
            "message": f"Generated and stored {len(addresses)} addresses."
        }
        self.storage.save_logs(log_entry)
    
    def run(self):
        """
        Executes the agent workflow: asks user questions, generates addresses, and stores them.
        """
        user_responses = self.ask_user_questions()
        addresses = self.generate_addresses(user_responses)
        self.save_generated_addresses(addresses)
        print("✅ Addresses successfully generated and stored!")
        
# Example usage
if __name__ == "__main__":
    agent = InitialInputGenerationAgent()
    agent.run()
