import requests
import os
import sys
from langchain.tools import Tool
from config.load_config import config

def search_real_addresses(query: str):
    """
    Searches the web for real addresses using the Tavily Search API.
    """
    api_key = os.getenv("TAVILY_API_KEY")  # Tavily API Key
    search_url = "https://api.tavily.com/search"  # Tavily Search API endpoint

    payload = {
        "query": query,
        "topic": "general",
        "search_depth": "basic",
        "max_results": 10,
        "time_range": None,
        "days": 3,
        "include_answer": False,
        "include_raw_content": False,
        "include_images": False,
        "include_image_descriptions": False,
        "include_domains": [],
        "exclude_domains": []
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", search_url, json=payload, headers=headers)
    return response.text

# Define the LangChain tool
AddressSearchTool = Tool(
    name="AddressSearchTool",
    func=search_real_addresses,
    description="A tool that searches real addresses using Search API based on user input."
)

if __name__ == "__main__":

    query = input("Please enter a search query: ")
    response = search_real_addresses(query)
    print(response)
    