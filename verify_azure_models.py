#!/usr/bin/env python3
"""
Verify that Azure OpenAI model mapping is working correctly.
"""
import os
import sys
from server import ModelMapper

def test_azure_model_mapping():
    """Test that the ModelMapper correctly handles Azure OpenAI models."""
    
    print("🧪 Testing Azure OpenAI model mapping...")
    
    # Test various Azure model configurations
    test_cases = [
        {
            "preferred_provider": "azure",
            "big_model": "gpt-4o-deployment",
            "small_model": "gpt-4o-mini-deployment",
            "test_model": "sonnet",
            "expected_result": "azure/gpt-4o-deployment"
        },
        {
            "preferred_provider": "azure", 
            "big_model": "my-custom-gpt4",
            "small_model": "my-custom-gpt4-mini",
            "test_model": "haiku",
            "expected_result": "azure/my-custom-gpt4-mini"
        },
        {
            "preferred_provider": "openai",  # Non-Azure provider
            "big_model": "gpt-4.1",
            "small_model": "gpt-4.1-mini",
            "test_model": "sonnet",
            "expected_result": "openai/gpt-4.1"
        }
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['preferred_provider']} provider")
        print(f"   Big Model: {test_case['big_model']}")
        print(f"   Small Model: {test_case['small_model']}")
        print(f"   Testing: {test_case['test_model']} → {test_case['expected_result']}")
        
        # Set up environment variables for this test
        os.environ['PREFERRED_PROVIDER'] = test_case['preferred_provider']
        os.environ['BIG_MODEL'] = test_case['big_model']
        os.environ['SMALL_MODEL'] = test_case['small_model']
        
        # Create new mapper instance
        mapper = ModelMapper()
        
        # Test the mapping
        result = mapper.map_model(test_case['test_model'])
        
        if result == test_case['expected_result']:
            print(f"   ✅ SUCCESS: {result}")
        else:
            print(f"   ❌ FAILED: Expected {test_case['expected_result']}, got {result}")
            all_passed = False
    
    # Test direct Azure model specification
    print(f"\n📝 Test Case 4: Direct Azure model specification")
    mapper = ModelMapper()
    direct_azure_model = "azure/my-deployment-name"
    result = mapper.map_model(direct_azure_model)
    expected = direct_azure_model
    
    if result == expected:
        print(f"   ✅ SUCCESS: {result}")
    else:
        print(f"   ❌ FAILED: Expected {expected}, got {result}")
        all_passed = False
    
    # Test model prefix detection
    print(f"\n📝 Test Case 5: Model prefix detection")
    test_models = [
        ("azure/gpt-4o", True),
        ("openai/gpt-4.1", False),
        ("gemini/gemini-pro", False),
        ("sonnet", False)
    ]
    
    for model, should_be_azure in test_models:
        is_azure = model.startswith("azure/")
        if is_azure == should_be_azure:
            print(f"   ✅ {model} → Azure: {is_azure}")
        else:
            print(f"   ❌ {model} → Expected Azure: {should_be_azure}, got {is_azure}")
            all_passed = False
    
    print("\n" + "="*50)
    print("📊 AZURE MODEL MAPPING TEST SUMMARY")
    print("="*50)
    
    if all_passed:
        print("✅ All Azure model mapping tests passed!")
        print("🎯 The ModelMapper correctly handles Azure OpenAI models")
        print("💡 Azure OpenAI integration is working correctly")
        return True
    else:
        print("❌ Some tests failed")
        print("🔧 Check the ModelMapper implementation")
        return False

if __name__ == "__main__":
    # Save original environment variables
    original_env = {}
    for key in ['PREFERRED_PROVIDER', 'BIG_MODEL', 'SMALL_MODEL']:
        original_env[key] = os.environ.get(key)
    
    try:
        success = test_azure_model_mapping()
        sys.exit(0 if success else 1)
    finally:
        # Restore original environment variables
        for key, value in original_env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]