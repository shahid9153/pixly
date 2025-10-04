"""
Test script to test the game knowledge base system and some API endpoints
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://127.0.0.1:8000"

def test_api_endpoint(endpoint, method="GET", data=None):
    """Test an API endpoint and return the response."""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            return {"error": f"Unsupported method: {method}"}
        
        return {
            "status_code": response.status_code,
            "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
        }
    except Exception as e:
        return {"error": str(e)}

def main():
    print("🎮 Game Knowledge Base System Test")
    print("=" * 50)
    
    # Test 1: Check if server is running
    print("\n1. Testing server connection...")
    result = test_api_endpoint("/games/list")
    if result.get("status_code") == 200:
        print("Server is running")
    else:
        print("Server is not running. Please start the server first:")
        print("uv run run.py")
        return
    
    # Test 2: List available games
    print("\n2. Testing game listing...")
    result = test_api_endpoint("/games/list")
    if result.get("status_code") == 200:
        games = result["response"]
        print(f"Available games:")
        print(f"Detection games: {games.get('detection_games', [])}")
        print(f"CSV games: {games.get('csv_games', [])}")
        print(f"Vector games: {games.get('vector_games', [])}")
    else:
        print(f"Failed to list games: {result}")
    
    # Test 3: Validate Minecraft CSV
    print("\n3. Testing Minecraft CSV validation...")
    result = test_api_endpoint("/games/minecraft/knowledge/validate")
    if result.get("status_code") == 200:
        validation = result["response"]
        if validation.get("is_valid"):
            print("Minecraft CSV is valid")
        else:
            print(f"Minecraft CSV validation failed: {validation.get('errors', [])}")
    else:
        print(f"Failed to validate CSV: {result}")
    
    # Test 4: Process Minecraft knowledge
    print("\n4. Processing Minecraft knowledge...")
    print("   This may take a few minutes as it extracts content from URLs...")
    result = test_api_endpoint("/games/minecraft/knowledge/process", "POST")
    if result.get("status_code") == 200:
        process_result = result["response"]
        print(f"Successfully processed Minecraft knowledge")
        print(f"Stats: {process_result.get('stats', {})}")
    else:
        print(f"Failed to process knowledge: {result}")
        return
    
    # Test 5: Search Minecraft knowledge
    print("\n5. Testing knowledge search...")
    search_queries = [
        "How to make redstone circuits?",
        "What are the best enchantments?",
        "How to find villagers?"
    ]
    
    for query in search_queries:
        print(f"\n   Searching: '{query}'")
        search_data = {
            "query": query,
            "limit": 3,
            "game_namme":"Minecraft"
        }
        result = test_api_endpoint("/games/minecraft/knowledge/search", "POST", search_data)
        if result.get("status_code") == 200:
            search_result = result["response"]
            print(f"Found {search_result.get('total_results', 0)} results")
            for i, res in enumerate(search_result.get('results', [])[:2], 1):
                print(f"{i}. {res.get('metadata', {}).get('title', 'Unknown')}")
                print(f"Source: {res.get('metadata', {}).get('content_type', 'unknown')}")
                print(f"Content: {res.get('content', '')[:100]}...")
        else:
            print(f"Search failed: {result}")
    
    # Test 6: Test game detection
    print("\n6. Testing game detection...")
    test_messages = [
        "I'm playing Minecraft and need help with redstone",
        "How do I beat this boss in Dark Souls?",
        "What's the best strategy for building in Minecraft?"
    ]
    
    for message in test_messages:
        print(f"\n   Testing: '{message}'")
        detect_data = {"message": message}
        result = test_api_endpoint("/games/detect", "POST", detect_data)
        if result.get("status_code") == 200:
            detect_result = result["response"]
            detected_game = detect_result.get("detected_game")
            print(f"Detected game: {detected_game}")
        else:
            print(f"Detection failed: {result}")
    
    # Test 7: Test enhanced chat
    print("\n7. Testing enhanced chat...")
    chat_messages = [
        "I need help with redstone in Minecraft",
        "What are the best enchantments for my sword?",
        "How do I build an automatic farm?"
    ]
    
    for message in chat_messages:
        print(f"\n   Chat: '{message}'")
        chat_data = {"message": message}
        result = test_api_endpoint("/chat", "POST", chat_data)
        if result.get("status_code") == 200:
            chat_result = result["response"]
            response_text = chat_result.get("response", "")
            print(f"Response: {response_text[:200]}...")
        else:
            print(f"Chat failed: {result}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")
    print("\nTo test manually:")
    print("1. Start the server: python -m backend.backend")
    print("2. Use the API endpoints or test with the overlay interface")
    print("3. Check the vector_db folder for stored embeddings")

if __name__ == "__main__":
    main()
