"""
Claude.ai Integration Wrapper for Vertex AI Delegation

This is called BY Claude.ai (me) to automatically delegate tasks to Vertex AI.
James doesn't need to run this manually - I call it through Desktop Commander.
"""

import sys
import json
from vertex_delegate import vertex_delegate

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No command specified"}))
        return
    
    command = sys.argv[1]
    
    if command == "component":
        # python vertex_wrapper.py component "ComponentName" "specs" "output/path.tsx"
        name = sys.argv[2]
        specs = sys.argv[3]
        output = sys.argv[4] if len(sys.argv) > 4 else None
        
        result = vertex_delegate.delegate_component(name, specs, output)
        print(json.dumps(result, indent=2))
        
    elif command == "blueprint":
        # python vertex_wrapper.py blueprint "blueprint-type" "output/path.md"
        blueprint_type = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else None
        
        result = vertex_delegate.delegate_blueprint(blueprint_type, output)
        print(json.dumps(result, indent=2))
        
    elif command == "batch":
        # python vertex_wrapper.py batch "tasks.json"
        tasks_file = sys.argv[2]
        with open(tasks_file, 'r') as f:
            tasks = json.load(f)
        
        result = vertex_delegate.delegate_batch(tasks)
        print(json.dumps(result, indent=2))
        
    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))

if __name__ == "__main__":
    main()
