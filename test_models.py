"""Quick test to find available Claude models"""
from anthropic import AnthropicVertex

PROJECT_ID = "einharjer-valhalla"
REGION = "us-east5"

models_to_test = [
    "claude-3-7-sonnet-20250219",
    "claude-sonnet-4-20250514",
    "claude-3-5-sonnet-20241022",
    "claude-3-opus-20240229",
]

print("Testing models...\n")

client = AnthropicVertex(project_id=PROJECT_ID, region=REGION)

for model in models_to_test:
    try:
        print(f"Testing: {model}...", end=" ")
        message = client.messages.create(
            model=model, max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"WORKS! --> {model}")
        break
    except Exception as e:
        if "404" in str(e):
            print("Not found")
        else:
            print(f"Error: {str(e)[:50]}")
