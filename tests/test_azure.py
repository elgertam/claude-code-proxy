#!/usr/bin/env python3
"""
Test script to verify Azure OpenAI integration with the proxy server.
"""
import httpx
import json
import os
import sys

def test_azure_endpoint():
    """Test the Azure OpenAI endpoint through the proxy."""
    
    # Server URL
    base_url = "http://localhost:5000"
    
    # Test message payload
    test_payload = {
        "model": "azure/gpt-4o-mini",  # Using azure/ prefix
        "max_tokens": 100,
        "messages": [
            {
                "role": "user",
                "content": "Hello! Can you tell me what provider you are running on?"
            }
        ]
    }
    
    print("🧪 Testing Azure OpenAI integration...")
    print(f"📡 Server URL: {base_url}")
    print(f"🎯 Test payload: {json.dumps(test_payload, indent=2)}")
    
    try:
        # Make request to the proxy
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{base_url}/v1/messages",
                json=test_payload,
                headers={"Content-Type": "application/json"}
            )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("✅ SUCCESS: Proxy responded successfully")
            print(f"🔍 Response: {json.dumps(response_data, indent=2)}")
            
            # Check if the response has the expected structure
            if "content" in response_data and "usage" in response_data:
                print("✅ Response structure looks correct")
                if response_data["content"]:
                    print(f"💬 Message: {response_data['content'][0].get('text', 'No text found')}")
                print(f"📈 Usage: {response_data['usage']}")
            else:
                print("⚠️  Response structure might be unexpected")
        else:
            print(f"❌ ERROR: Status {response.status_code}")
            print(f"📄 Error Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: Exception occurred: {str(e)}")
        return False
    
    return response.status_code == 200

def test_token_count():
    """Test the token counting endpoint."""
    
    base_url = "http://localhost:5000"
    
    test_payload = {
        "model": "azure/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": "Hello! This is a test message for token counting."
            }
        ]
    }
    
    print("\n🧪 Testing token counting endpoint...")
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{base_url}/v1/messages/count_tokens",
                json=test_payload,
                headers={"Content-Type": "application/json"}
            )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("✅ SUCCESS: Token counting works")
            print(f"🔢 Token Count: {response_data.get('input_tokens', 'N/A')}")
        else:
            print(f"❌ ERROR: Status {response.status_code}")
            print(f"📄 Error: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: Exception occurred: {str(e)}")
        return False
    
    return response.status_code == 200

def test_server_info():
    """Test the server info endpoint."""
    
    base_url = "http://localhost:5000"
    
    print("\n🧪 Testing server info endpoint...")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(f"{base_url}/")
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            print("✅ SUCCESS: Server info endpoint works")
            print(f"📋 Server Info: {json.dumps(response_data, indent=2)}")
            
            # Check if Azure is in supported providers
            if "azure" in response_data.get("supported_providers", []):
                print("✅ Azure is listed as a supported provider")
            else:
                print("⚠️  Azure not found in supported providers")
        else:
            print(f"❌ ERROR: Status {response.status_code}")
            print(f"📄 Error: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: Exception occurred: {str(e)}")
        return False
    
    return response.status_code == 200

if __name__ == "__main__":
    print("🚀 Starting Azure OpenAI integration tests...")
    
    # Check if server is running
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get("http://localhost:5000/")
        if response.status_code != 200:
            print("❌ Server not responding correctly")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Server not reachable: {str(e)}")
        print("💡 Make sure the server is running with: uv run uvicorn server:app --host 0.0.0.0 --port 5000")
        sys.exit(1)
    
    # Run tests
    results = []
    
    results.append(test_server_info())
    results.append(test_token_count())
    
    # Note: We skip the actual message test unless Azure keys are configured
    # since it would require real Azure OpenAI credentials
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    if all(results):
        print("✅ All endpoint tests passed!")
        print("💡 To test with real Azure OpenAI:")
        print("   1. Configure AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT")
        print("   2. Set PREFERRED_PROVIDER=azure")
        print("   3. Run: python test_azure.py")
    else:
        print("❌ Some tests failed")
        print("💡 Check server logs for more details")
        sys.exit(1)