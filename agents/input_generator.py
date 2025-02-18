from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from tools.PlacesSearchTool import PlacesSearchTool
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
        """Initialize the agent with the LLM and required tools."""
        open_api_key = os.getenv('OPEN_API_KEY')  # Retrieve the API key from environment variables
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature, api_key=open_api_key)
        self.memory = ConversationBufferMemory()
        self.tools = [PlacesSearchTool]
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )
        self.storage = JSONStorageHandler()

    def ask_user_questions(self):
        """
        Ask user 2-3 questions to infer address details.
        """
        questions = [
            "Which city or region should the addresses be from?",
            "How big of a radius should we search for addresses?",
            "What type of addresses should we search for?"
        ]
        
        responses = {}
        for question in questions:
            response = input(f"{question} ")
            responses[question] = response
            
        return responses
    
    def create_search_query(self, user_responses):
        """Create a search query based on user responses using the LLM."""
        query_prompt = f"Based on these parameters:\n" \
                      f"- Location: {user_responses['Which city or region should the addresses be from?']}\n" \
                      f"- Radius: {user_responses['How big of a radius should we search for addresses?']}\n" \
                      f"- Type: {user_responses['What type of addresses should we search for?']}\n\n" \
                      f"Create a text search query to be passed to Google Places API that will return relevant addresses. " \
                      f"Iterate on the query at least 10 times or more until you get a good balance of specificity and breadth that will return the best matches from the Google Places API. " \
                      f"Do not include any additional infromation from your reasoning only the pure query that will be passed to the Google Places API." \
                      f"The query should be in natural language and not a URL call." \
                      f"Do not include any additional information in the query (e.g. API key, etc.)"

        response = self.llm.invoke(query_prompt)
        return response.content

    def generate_addresses(self, user_responses):
        """
        Uses LLM to generate synthetic address data based on user responses.
        """
        # First, create a search query based on user responses
        search_query = self.create_search_query(user_responses)
        print(f"Generated search query: {search_query}")

        # Use the PlacesSearchTool to get real address data
        try:
            places_result = self.tools[0].func(search_query)
            places_data = json.loads(places_result)
            
         # Loop through all results and map them into the expected format
            formatted_addresses = []
            for place in places_data.get("results", []):  # Extracting the list of places

                formatted_addresses.append({
                    "original_address": place.get("formatted_address", ""),
                })

            print("FORMATTED ADDRESSES: ", formatted_addresses)
            return formatted_addresses  # Return the list of formatted addresses
            
        except Exception as e:
            log_entry = {
                "timestamp": datetime.now(pytz.utc).isoformat(),
                "agent": "Initial Input Generation Agent",
                "message": f"Error: Failed to process places search. {e}"
            }
            self.storage.save_logs(log_entry)
            return []
  
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
