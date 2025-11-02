"""Test with direct REST API call"""
import requests

api_key = "AQ.Ab8RN6KYsm18q1hXK5AAok5sdkza_nfuyrzslLL33ChHFxtPqw"
url = "https://aiplatform.googleapis.com/v1/publishers/google/models/gemini-2.5-flash-lite:streamGenerateContent"

# Try the URL from the screenshot
url2 = "https://aiplatform.googleapis.com/v1/publishers/anthropic/models/claude-opus-4.1:predict"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "prompt": "Say hello",
    "max_tokens": 10
}

try:
    response = requests.post(url2, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
