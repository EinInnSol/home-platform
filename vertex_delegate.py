"""
Vertex AI Delegation System for Claude.ai

This allows Claude (me) to automatically delegate code generation
to Vertex AI after we agree on a decision, without you having to
run manual Python scripts.

Usage: Called by Claude.ai Desktop Commander
"""

from anthropic import AnthropicVertex
import json
import os
from datetime import datetime
from pathlib import Path

class VertexDelegate:
    """Automated delegation system to Vertex AI"""
    
    def __init__(self, project_root="C:\\Users\\james\\Projects\\Active\\home-platform"):
        self.project_id = "einharjer-valhalla"
        self.region = "us-east5"
        self.api_key = "AQ.Ab8RN6KYsm18q1hXK5AAok5sdkza_nfuyrzslLL33ChHFxtPqw"
        self.client = None
        self.project_root = Path(project_root)
        self.log_file = self.project_root / "vertex_delegations.log"
        
    def connect(self):
        """Connect to Vertex AI"""
        if self.client:
            return True
            
        try:
            self.client = AnthropicVertex(
                project_id=self.project_id,
                region=self.region
            )
            self._log("[OK] Connected to Vertex AI")
            return True
        except Exception as e:
            self._log(f"[ERROR] Connection failed: {e}")
            return False
    
    def delegate_component(self, component_name, specifications, output_path=None):
        """
        Delegate component generation to Vertex AI
        
        Args:
            component_name: Name of the component (e.g., "IntakeForm")
            specifications: Detailed specs for the component
            output_path: Optional path to save the generated code
            
        Returns:
            dict with 'success', 'code', 'tokens', 'cost_estimate'
        """
        if not self.connect():
            return {"success": False, "error": "Failed to connect to Vertex AI"}
        
        self._log(f"\n[ROBOT] Delegating: {component_name}")
        self._log(f"   Specs: {specifications[:100]}...")
        
        prompt = self._build_component_prompt(component_name, specifications)
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            code = message.content[0].text
            tokens = message.usage.input_tokens + message.usage.output_tokens
            cost = self._estimate_cost(message.usage.input_tokens, message.usage.output_tokens)
            
            self._log(f"[OK] Generated ({tokens} tokens, ~${cost:.3f})")
            
            # Save if output path provided
            if output_path:
                full_path = self.project_root / output_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(code, encoding='utf-8')
                self._log(f"[SAVED] Saved to: {output_path}")
            
            return {
                "success": True,
                "code": code,
                "tokens": tokens,
                "cost_estimate": cost,
                "saved_to": str(output_path) if output_path else None
            }
            
        except Exception as e:
            self._log(f"[ERROR] Generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    def delegate_blueprint(self, blueprint_type, output_path=None):
        """Delegate blueprint generation to Vertex AI"""
        
        blueprints = {
            "intake-form": "Complete mobile-first intake form with 40 HUD questions, validation, auto-save, and progress tracking",
            "caseworker-dashboard": "Caseworker dashboard with action queue, client list, filters, and real-time updates",
            "city-dashboard": "City analytics dashboard with real-time metrics, charts, and HUD compliance tracking",
            "api-layer": "Complete API integration layer with Axios, error handling, and TypeScript types"
        }
        
        if blueprint_type not in blueprints:
            return {"success": False, "error": f"Unknown blueprint: {blueprint_type}"}
        
        if not self.connect():
            return {"success": False, "error": "Failed to connect to Vertex AI"}
        
        self._log(f"\n[BLUEPRINT] Delegating blueprint: {blueprint_type}")
        
        prompt = self._build_blueprint_prompt(blueprint_type, blueprints[blueprint_type])
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            blueprint = message.content[0].text
            tokens = message.usage.input_tokens + message.usage.output_tokens
            cost = self._estimate_cost(message.usage.input_tokens, message.usage.output_tokens)
            
            self._log(f"[OK] Blueprint generated ({tokens} tokens, ~${cost:.3f})")
            
            if output_path:
                full_path = self.project_root / output_path
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.write_text(blueprint, encoding='utf-8')
                self._log(f"[SAVED] Saved to: {output_path}")
            
            return {
                "success": True,
                "blueprint": blueprint,
                "tokens": tokens,
                "cost_estimate": cost,
                "saved_to": str(output_path) if output_path else None
            }
            
        except Exception as e:
            self._log(f"[ERROR] Blueprint generation failed: {e}")
            return {"success": False, "error": str(e)}
    
    def delegate_batch(self, tasks):
        """
        Delegate multiple tasks at once
        
        Args:
            tasks: List of dicts with 'type', 'name', 'specs', 'output'
            
        Example:
            tasks = [
                {'type': 'component', 'name': 'Header', 'specs': '...', 'output': 'src/components/Header.tsx'},
                {'type': 'component', 'name': 'Footer', 'specs': '...', 'output': 'src/components/Footer.tsx'}
            ]
        """
        results = []
        total_cost = 0
        
        self._log(f"\n[BATCH] Batch delegation: {len(tasks)} tasks")
        
        for i, task in enumerate(tasks, 1):
            self._log(f"\n[{i}/{len(tasks)}] Processing: {task.get('name', 'unknown')}")
            
            if task['type'] == 'component':
                result = self.delegate_component(
                    task['name'],
                    task['specs'],
                    task.get('output')
                )
            elif task['type'] == 'blueprint':
                result = self.delegate_blueprint(
                    task['name'],
                    task.get('output')
                )
            else:
                result = {"success": False, "error": f"Unknown task type: {task['type']}"}
            
            results.append(result)
            if result.get('success'):
                total_cost += result.get('cost_estimate', 0)
        
        self._log(f"\n[OK] Batch complete! Total cost: ~${total_cost:.2f}")
        
        return {
            "success": True,
            "results": results,
            "total_cost": total_cost,
            "successful": sum(1 for r in results if r.get('success')),
            "failed": sum(1 for r in results if not r.get('success'))
        }
    
    def _build_component_prompt(self, component_name, specs):
        """Build prompt for component generation"""
        return f"""You are a senior full-stack developer building the H.O.M.E. Platform for Long Beach homeless services.

PROJECT CONTEXT:
- Platform: Housing Opportunity Management Engine (H.O.M.E.)
- Demo Date: November 15, 2025
- Goal: Win $75K pilot contract
- Tech Stack: React 18 + TypeScript + Vite + Tailwind CSS + FastAPI backend
- Focus: Mobile-first, HUD-compliant, accessible

TASK: Generate a complete React component

COMPONENT NAME: {component_name}

SPECIFICATIONS:
{specs}

REQUIREMENTS:
1. TypeScript with proper interfaces/types
2. Tailwind CSS for all styling (mobile-first)
3. Accessibility (WCAG 2.1 AA compliant)
4. Error handling and loading states
5. Clean, well-commented code
6. React best practices (hooks, no class components)
7. Ready to drop into the project

OUTPUT FORMAT:
Provide ONLY the complete component code, ready to save as a .tsx file.
Include all imports, interfaces, the component, and default export.
Do not include explanations outside the code comments.

Generate the component now:"""

    def _build_blueprint_prompt(self, blueprint_type, description):
        """Build prompt for blueprint generation"""
        return f"""You are the technical architect for the H.O.M.E. Platform.

PROJECT: Housing Opportunity Management Engine
DEMO: November 15, 2025
GOAL: $75K Long Beach pilot contract

TASK: Create detailed technical blueprint

BLUEPRINT: {blueprint_type}
DESCRIPTION: {description}

PROVIDE:
1. Component architecture (files, folders, structure)
2. Key components with responsibilities
3. State management approach
4. Data flow and API integration
5. TypeScript interfaces
6. Implementation steps
7. Testing strategy
8. Performance considerations

Make it actionable and specific to our React + TypeScript + Tailwind stack.

Generate the blueprint now:"""
    
    def _estimate_cost(self, input_tokens, output_tokens):
        """Estimate cost based on Vertex AI pricing"""
        # Vertex AI Claude Sonnet pricing (approximate)
        input_cost = (input_tokens / 1_000_000) * 3.0
        output_cost = (output_tokens / 1_000_000) * 15.0
        return input_cost + output_cost
    
    def _log(self, message):
        """Log to file and print"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        # Print with UTF-8 encoding support
        try:
            print(log_message)
        except UnicodeEncodeError:
            # Fallback for Windows console
            print(log_message.encode('ascii', 'replace').decode('ascii'))
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + "\n")

# Global instance for easy access
vertex_delegate = VertexDelegate()
