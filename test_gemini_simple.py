"""Quick test of Gemini 2.5 Flash."""
import google.generativeai as genai

genai.configure(api_key="AIzaSyC2nBT65jo8vyLAUYrINmKegfDhGlF0a54")

print("Testing gemini-2.5-flash...")
model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content("Say 'Hello from Gemini 2.5 Flash!'")
print(f"✅ Response: {response.text}")
