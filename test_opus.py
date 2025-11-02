"""Test more model variations"""
from anthropic import AnthropicVertex

models = [
    "claude-opus-4.1",
    "claude-4.1-opus",
    "claude-opus@4.1",
    "anthropic.claude-opus-4.1",
    "publishers/anthropic/models/claude-opus-4.1",
]

client = AnthropicVertex(project_id="einharjer-valhalla", region="us-east5")

for model in models:
    try:
        print(f"{model}...", end=" ")
        msg = client.messages.create(model=model, max_tokens=10, messages=[{"role": "user", "content": "Hi"}])
        print(f"WORKS! --> Use: {model}")
        break
    except Exception as e:
        print("no")
