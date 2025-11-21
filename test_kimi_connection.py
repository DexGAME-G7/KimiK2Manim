import os
import asyncio
from kimi_client import get_kimi_client

async def test_api():
    print("Testing Kimi API connectivity...")
    
    api_key = os.getenv("MOONSHOT_API_KEY")
    if not api_key:
        print("Error: MOONSHOT_API_KEY not found in environment.")
        return

    # Mask key for display
    masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "***"
    print(f"Using API Key: {masked_key}")
    
    client = get_kimi_client()
    
    try:
        print("Sending simple 'Hello' request...")
        response = client.chat_completion(
            messages=[{"role": "user", "content": "Hello! Are you working?"}],
            max_tokens=50,
            temperature=0.7
        )
        
        content = client.get_text_content(response)
        print("\nAPI Response Success:")
        print(f"Content: {content}")
        
    except Exception as e:
        print(f"\nAPI Connection Failed:")
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())

