"""
Quick delegation script for VI-SPDAT form generation
"""
from vertex_delegate import vertex_delegate

# Generate the VI-SPDAT intake form - Section A: Housing History
task_specs = """
Create a React component for VI-SPDAT Section A: Housing History

This section has 3 questions from the official VI-SPDAT v2.0:

1. "Where do you sleep most frequently?"
   - Options: Shelters, Transitional Housing, Safe Haven, Outdoors, Other (text), Refused
   - Scoring: 1 point if NOT Shelters/Transitional/Safe Haven

2. "How long has it been since you lived in permanent stable housing?"
   - Free text input for duration
   - Not scored directly

3. "In the last three years, how many times have you been homeless?"
   - Number input
   - Scoring: 1 point if 1+ consecutive years OR 4+ episodes
   - Combined with Q2 for scoring

REQUIREMENTS:
- Mobile-first design with Tailwind CSS
- Radio buttons for Q1
- Text input for Q2
- Number input for Q3
- "Refused" option for each question
- Progress indicator showing Section A of 5 sections
- Next/Back navigation buttons
- Form validation
- State management with React hooks
- TypeScript interfaces for data
- Save progress on each answer
- Accessible (ARIA labels, keyboard navigation)

The component should:
1. Accept onNext/onBack callbacks
2. Track all answers in local state
3. Pass answers up to parent on navigation
4. Show validation errors
5. Auto-save to localStorage
6. Be part of a multi-step form flow
"""

print("Delegating VI-SPDAT Section A generation to Vertex AI...")
print("This will cost approximately $0.10-0.15")
print()

result = vertex_delegate.delegate_component(
    component_name="SectionA_HousingHistory",
    specifications=task_specs,
    output_path="frontend/app/assessment/SectionA_HousingHistory.tsx"
)

if result['success']:
    print("\n✅ SUCCESS!")
    print(f"   Component generated: {result['tokens']} tokens")
    print(f"   Cost: ${result['cost_estimate']:.3f}")
    print(f"   Saved to: {result['saved_to']}")
    print("\nComponent is ready to use!")
else:
    print(f"\n❌ FAILED: {result.get('error')}")
