"""Test script to find available Gemini models."""
import google.generativeai as genai

# Configure with your API key
genai.configure(api_key="AIzaSyC2nBT65jo8vyLAUYrINmKegfDhGlF0a54")

print("🔍 Listing available Gemini models...\n")

# List all available models
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ Model: {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Description: {model.description}")
        print()

print("\n🧪 Testing a simple generation...\n")

# Try the most common model names
model_names_to_try = [
    "gemini-pro",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "models/gemini-pro",
    "models/gemini-1.5-pro",
    "models/gemini-1.5-flash"
]

for model_name in model_names_to_try:
    try:
        print(f"Trying: {model_name}...")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Hello, this model works!'")
        print(f"✅ SUCCESS with {model_name}")
        print(f"   Response: {response.text}")
        print()
        break
    except Exception as e:
        print(f"❌ Failed: {str(e)[:100]}")
        print()
