from agents.input_generator import InitialInputGenerationAgent

def test_agent():
    # Initialize the agent
    agent = InitialInputGenerationAgent()
    
    # Simulate user responses
    test_responses = {
        "Which city or region should the addresses be from?": "Chicago downtown",
        "Do you need residential, commercial, or mixed-type addresses?": "commercial",
        "Should we include apartment buildings and units? (Yes/No)": "No"
    }
    
    # Generate addresses
    addresses = agent.generate_addresses(test_responses)
    
    # Print results
    print("\nGenerated Addresses:")
    print(json.dumps(addresses, indent=2))

if __name__ == "__main__":
    test_agent()
