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
        
        # Get the first result (most relevant to validate the structuring of response. Turn this into a loop to get all results)
        if places_result.get('results'):
            place = places_result['results'][0]
            
            # Create the response structure
            place_data = {
                "place": {
                    "basic_info": {
                        "name": place.get('name', ''),
                        "place_id": place.get('place_id', ''),
                        "types": place.get('types', [])
                    },
                    "address": {
                        "formatted": place.get('formatted_address', ''),
                        "components": place.get('address_components', [])
                    },
                    "location": {
                        "coordinates": place.get('geometry', {}).get('location', {}),
                        "viewport": place.get('geometry', {}).get('viewport', {})
                    },
                    "business": {
                        "status": place.get('business_status', ''),
                        "rating": place.get('rating', None),
                        "user_ratings_total": place.get('user_ratings_total', 0),
                        "price_level": place.get('price_level', None)
                    }
                }
            }
            
            # Get additional place details
            if place.get('place_id'):
                try:
                    place_details = gmaps.place(
                        place['place_id'],
                        fields=[
                            'formatted_phone_number',
                            'website',
                            'opening_hours'
                        ]
                    )
                    
                    if place_details.get('result'):
                        details = place_details['result']
                        place_data["place"]["contact"] = {
                            "phone": details.get('formatted_phone_number', ''),
                            "website": details.get('website', '')
                        }
                        
                        place_data["place"]["hours"] = {
                            "open_now": details.get('opening_hours', {}).get('open_now', None),
                            "periods": details.get('opening_hours', {}).get('periods', [])
                        }
                        
                except Exception as detail_error:
                    place_data["place"]["errors"] = {
                        "detail_fetch_error": str(detail_error)
                    }
            
            # Clean and sanitize the response
            cleaned_response = clean_dict(place_data)
            
            # Return formatted JSON string
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
    with open('search_results.json', 'w', encoding='utf-8') as f:
        f.write(response)
    