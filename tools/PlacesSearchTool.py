import os
import json
from typing import Dict, List
import googlemaps
from langchain.tools import Tool
from config.load_config import config

def clean_value(value):
    """Clean and sanitize values for JSON encoding"""
    if isinstance(value, str):
        return value.replace('\n', ' ').replace('\r', ' ').strip()
    return value

def clean_dict(data):
    """Recursively clean dictionary values for JSON encoding"""
    if isinstance(data, dict):
        return {k: clean_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_dict(item) for item in data]
    return clean_value(data)

def search_places(query: str) -> str:
    """
    Searches for places and addresses using Google Maps Places API.
    Args:
        query (str): Search query for finding places/addresses
    Returns:
        str: Formatted JSON string with place information
    """
    try:
        # Initialize Google Maps client
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        gmaps = googlemaps.Client(key=api_key)
        
        # Perform place search
        places_result = gmaps.places(
            query,
            language="en",
            type=None
        )
        
        if places_result:
            cleaned_response = clean_dict(places_result)
            return json.dumps(cleaned_response, ensure_ascii=False, indent=2)
        else:
            return json.dumps({"error": "No places found for the query"}, indent=2)
            
    except Exception as e:
        error_response = {
            "error": {
                "message": clean_value(str(e)),
                "query": clean_value(query)
            }
        }
        return json.dumps(error_response, indent=2)

# Define the LangChain tool
PlacesSearchTool = Tool(
    name="PlacesSearchTool",
    func=search_places,
    description="""A tool that searches for places and addresses using Google Maps Places API. 
    Returns a hierarchically structured JSON with detailed place information for the most relevant result."""
)

if __name__ == "__main__":
    #query = input("Please enter a search query: ")
    query = "search all mcdonalds restaurants in chicago"
    response = search_places(query)
    
    # Write the response to a JSON file
    storage_path = config.STORAGE_PATH
    file_path = os.path.join(storage_path, 'search_results.json')
    print(f"Writing response to {file_path}")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(response)    
