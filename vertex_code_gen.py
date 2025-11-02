"""
H.O.M.E. Platform - Vertex AI Claude Code Generator
Cost-Efficient Blueprint Builder

This tool uses Google Vertex AI's Claude to generate code blueprints,
saving your Claude.ai rate limits for strategic decisions.

USAGE:
    python vertex_code_gen.py --component "IntakeForm" --specs "mobile-first React component"
    python vertex_code_gen.py --blueprint "caseworker-dashboard"
    python vertex_code_gen.py --refactor "src/components/intake/IntakeForm.tsx"
"""

from anthropic import AnthropicVertex
import argparse
import os
import json
from pathlib import Path

class VertexCodeGenerator:
    """Generate code using Vertex AI Claude"""
    
    def __init__(self):
        self.project_id = "einharjer-valhalla"
        self.region = "us-east5"
        self.client = None
        self.project_context = self._load_project_context()
        
    def _load_project_context(self):
        """Load project context for better code generation"""
        return {
            "project": "H.O.M.E. Platform",
            "demo_date": "November 15, 2025",
            "tech_stack": {
                "frontend": "React 18 + TypeScript + Vite + Tailwind CSS",
                "backend": "FastAPI + Python 3.11 + GCP Firestore",
                "deployment": "GCP Cloud Run"
            },
            "mvp_features": [
                "Mobile intake form (40 HUD questions)",
                "VI-SPDAT auto-scoring",
                "Caseworker dashboard",
                "City analytics dashboard"
            ]
        }
    
    def connect(self):
        """Connect to Vertex AI"""
        try:
            print(f"🔌 Connecting to Vertex AI...")
            print(f"   Project: {self.project_id}")
            print(f"   Region: {self.region}")
            
            self.client = AnthropicVertex(
                project_id=self.project_id,
                region=self.region
            )
            
            print("✅ Connected to Vertex AI Claude!")
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            print("\n🔧 Troubleshooting:")
            print("   1. Install: pip install anthropic[vertex]")
            print("   2. Run: gcloud auth application-default login")
            print("   3. Verify billing is enabled")
            return False
    
    def generate_component(self, component_name, specs):
        """Generate a React component"""
        
        prompt = f"""You are a senior React developer building the H.O.M.E. Platform.

PROJECT CONTEXT:
{json.dumps(self.project_context, indent=2)}

TASK: Generate a complete React component

COMPONENT: {component_name}
SPECIFICATIONS: {specs}

REQUIREMENTS:
1. Use TypeScript
2. Use Tailwind CSS for styling
3. Mobile-first responsive design
4. Include proper TypeScript interfaces
5. Add helpful comments
6. Follow React best practices
7. Include error handling

OUTPUT FORMAT:
Provide the complete component code ready to save as a .tsx file.
Include imports, types, component, and export.

Generate the code now:"""

        return self._call_claude(prompt, max_tokens=4000)
    
    def generate_blueprint(self, blueprint_type):
        """Generate architectural blueprint"""
        
        blueprints = {
            "intake-form": "Complete mobile-first intake form with 40 HUD questions, validation, and auto-save",
            "caseworker-dashboard": "Caseworker dashboard with action queue, client list, and metrics",
            "city-dashboard": "City analytics dashboard with real-time metrics and charts",
            "api-integration": "API integration layer with Axios for backend communication"
        }
        
        if blueprint_type not in blueprints:
            print(f"❌ Unknown blueprint: {blueprint_type}")
            print(f"   Available: {', '.join(blueprints.keys())}")
            return None
        
        prompt = f"""You are the technical architect for H.O.M.E. Platform.

PROJECT CONTEXT:
{json.dumps(self.project_context, indent=2)}

TASK: Create detailed blueprint for {blueprint_type}

DESCRIPTION: {blueprints[blueprint_type]}

BLUEPRINT SHOULD INCLUDE:
1. Component structure (files and folders)
2. Key components with responsibilities
3. State management approach
4. API integration points
5. Data flow
6. TypeScript interfaces
7. Implementation steps

Provide a comprehensive blueprint:"""

        return self._call_claude(prompt, max_tokens=3000)
    
    def refactor_code(self, file_path):
        """Refactor existing code"""
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        prompt = f"""You are a code review expert for the H.O.M.E. Platform project.

PROJECT CONTEXT:
{json.dumps(self.project_context, indent=2)}

TASK: Review and refactor this code

FILE: {file_path}

CURRENT CODE:
```
{code}
```

REFACTOR FOR:
1. Performance improvements
2. Better TypeScript types
3. Code organization
4. Error handling
5. Accessibility
6. Mobile optimization
7. Best practices

Provide the refactored code:"""

        return self._call_claude(prompt, max_tokens=4000)
    
    def _call_claude(self, prompt, max_tokens=2000):
        """Call Claude via Vertex AI"""
        
        if not self.client:
            if not self.connect():
                return None
        
        try:
            print(f"\n🤖 Asking Vertex AI Claude...")
            
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            response = message.content[0].text
            
            tokens = message.usage.input_tokens + message.usage.output_tokens
            print(f"✅ Response received ({tokens} tokens)")
            
            return response
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description='Generate code using Vertex AI Claude')
    parser.add_argument('--component', help='Component name to generate')
    parser.add_argument('--specs', help='Component specifications')
    parser.add_argument('--blueprint', help='Blueprint type to generate')
    parser.add_argument('--refactor', help='File path to refactor')
    parser.add_argument('--output', help='Output file path')
    
    args = parser.parse_args()
    
    gen = VertexCodeGenerator()
    result = None
    
    if args.component and args.specs:
        result = gen.generate_component(args.component, args.specs)
        
    elif args.blueprint:
        result = gen.generate_blueprint(args.blueprint)
        
    elif args.refactor:
        result = gen.refactor_code(args.refactor)
    
    else:
        parser.print_help()
        return
    
    if result:
        print("\n" + "="*60)
        print(result)
        print("="*60)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"\n💾 Saved to: {args.output}")

if __name__ == "__main__":
    main()
