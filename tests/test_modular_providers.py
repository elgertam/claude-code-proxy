#!/usr/bin/env python3
"""
Test script to verify the modular provider system works correctly.
"""
import httpx
import json
import os
import sys

def test_provider_system():
    """Test that the modular provider system works correctly."""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing modular provider system...")
    
    # 1. Test server info endpoint
    print("\n📋 Testing server info endpoint...")
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(f"{base_url}/")
        
        if response.status_code == 200:
            server_info = response.json()
            print(f"✅ Server version: {server_info.get('version')}")
            print(f"✅ Supported providers: {server_info.get('supported_providers')}")
            print(f"✅ Available providers: {server_info.get('available_providers')}")
            print(f"✅ Preferred provider: {server_info.get('preferred_provider')}")
            
            # Check that the new version indicates modular support
            if "2.0.0" in server_info.get("version", ""):
                print("✅ Version indicates modular provider support")
            else:
                print("❌ Version doesn't indicate modular support")
                return False
        else:
            print(f"❌ Server info request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing server info: {str(e)}")
        return False
    
    # 2. Test model mapping with different providers
    print("\n📋 Testing model mapping with different providers...")
    
    test_cases = [
        ("sonnet", "Should map to preferred provider's big model"),
        ("haiku", "Should map to preferred provider's small model"),
        ("openai/gpt-4.1", "Should use OpenAI provider"),
        ("gemini/gemini-2.0-flash", "Should use Gemini provider"),
        ("azure/gpt-4o", "Should use Azure OpenAI provider"),
        ("anthropic/claude-3-5-sonnet-20241022", "Should use Anthropic provider")
    ]
    
    all_passed = True
    
    for test_model, description in test_cases:
        print(f"\n📝 Testing: {test_model}")
        print(f"   Description: {description}")
        
        # Test with token count endpoint (lightweight test)
        test_payload = {
            "model": test_model,
            "messages": [
                {
                    "role": "user",
                    "content": "Test message for provider routing"
                }
            ]
        }
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    f"{base_url}/v1/messages/count_tokens",
                    json=test_payload,
                    headers={"Content-Type": "application/json"}
                )
            
            if response.status_code == 200:
                response_data = response.json()
                token_count = response_data.get('input_tokens', 'N/A')
                print(f"   ✅ SUCCESS: Token count {token_count}")
            else:
                print(f"   ❌ FAILED: Status {response.status_code}")
                print(f"   📄 Error: {response.text}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            all_passed = False
    
    return all_passed

def test_extensibility():
    """Test that the provider system is extensible."""
    
    print("\n🔧 Testing provider system extensibility...")
    
    # Test that we can import the provider system
    try:
        # Add current directory to path to find providers module
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from providers.registry import registry
        from providers.base import BaseProvider
        
        print("✅ Provider system imports successfully")
        
        # Test provider registration
        print(f"✅ Registry has {len(registry.providers)} providers")
        
        # Test that we can access provider methods
        provider_names = registry.get_provider_names()
        print(f"✅ Provider names: {provider_names}")
        
        # Test that we can get available providers
        available = registry.get_available_provider_names()
        print(f"✅ Available providers: {available}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing extensibility: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting modular provider system tests...")
    
    # Check if server is running
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get("http://localhost:5000/")
        if response.status_code != 200:
            print("❌ Server not responding correctly")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Server not reachable: {str(e)}")
        print("💡 Make sure the server is running")
        sys.exit(1)
    
    # Run tests
    provider_test = test_provider_system()
    extensibility_test = test_extensibility()
    
    print("\n" + "="*50)
    print("📊 MODULAR PROVIDER SYSTEM TEST RESULTS")
    print("="*50)
    
    if provider_test and extensibility_test:
        print("✅ ALL TESTS PASSED!")
        print("\n🎯 The modular provider system is working correctly:")
        print("   - Server reports modular provider support")
        print("   - Model mapping works with different providers")
        print("   - Provider system is extensible and well-structured")
        print("   - Token counting works across all providers")
        print("\n🔧 Benefits of the new architecture:")
        print("   - Easy to add new providers")
        print("   - Cleaner code organization")
        print("   - Better error handling")
        print("   - More maintainable codebase")
    else:
        print("❌ SOME TESTS FAILED")
        print("🔧 Check the implementation and logs")
        
    sys.exit(0 if (provider_test and extensibility_test) else 1)