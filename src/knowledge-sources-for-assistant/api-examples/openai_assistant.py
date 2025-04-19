import os
import json
import openai
from typing import List, Dict, Any
from datetime import datetime

# Initialize OpenAI client
client = openai.OpenAI()

class PromptEngineeringAssistant:
    def __init__(self):
        """Initialize the Prompt Engineering Teaching Assistant"""
        self.assistant = self._create_assistant()
        self.thread = None
        self.current_run = None

    def _create_assistant(self) -> Any:
        """Create or load the OpenAI Assistant with custom configurations"""
        # Define the assistant's custom functions
        functions = [
            {
                "name": "analyzePrompt",
                "description": "Analyze a prompt and provide feedback on its structure and effectiveness",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The prompt to analyze"
                        },
                        "context": {
                            "type": "string",
                            "description": "The context in which the prompt will be used"
                        }
                    },
                    "required": ["prompt"]
                }
            },
            {
                "name": "generateExample",
                "description": "Generate an example prompt and response for a specific use case",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "The topic or concept to generate an example for"
                        },
                        "difficulty": {
                            "type": "string",
                            "enum": ["beginner", "intermediate", "advanced"],
                            "description": "The difficulty level of the example"
                        }
                    },
                    "required": ["topic"]
                }
            },
            {
                "name": "assessLearning",
                "description": "Assess student understanding of prompt engineering concepts",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "concept": {
                            "type": "string",
                            "description": "The concept to assess"
                        },
                        "submission": {
                            "type": "string",
                            "description": "The student's submission or answer"
                        }
                    },
                    "required": ["concept", "submission"]
                }
            }
        ]

        # Create the assistant
        assistant = client.beta.assistants.create(
            name="Prompt Engineering Teacher",
            instructions="""You are an expert prompt engineering teacher, designed to help students learn and master the art of crafting effective prompts for AI systems. Your approach should be:

1. Educational: Always explain the reasoning behind your suggestions
2. Interactive: Engage students with questions and exercises
3. Practical: Use real-world examples and applications
4. Supportive: Provide constructive feedback and encouragement

When analyzing prompts, consider:
- Clarity and specificity
- Structure and format
- Context and constraints
- Potential edge cases
- Best practices and common pitfalls""",
            model="gpt-4-1106-preview",
            tools=[{"type": "function", "function": f} for f in functions]
        )

        return assistant

    def start_conversation(self) -> None:
        """Start a new conversation thread"""
        self.thread = client.beta.threads.create()

    def send_message(self, message: str) -> Dict[str, Any]:
        """Send a message and get the assistant's response"""
        if not self.thread:
            self.start_conversation()

        # Add the user's message to the thread
        message = client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )

        # Run the assistant
        self.current_run = client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )

        # Wait for completion
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=self.current_run.id
            )
            if run_status.status == 'completed':
                break
            elif run_status.status == 'requires_action':
                self._handle_required_actions(run_status)

        # Get the assistant's response
        messages = client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        
        # Return the latest assistant message
        return {
            "role": messages.data[0].role,
            "content": messages.data[0].content[0].text.value
        }

    def _handle_required_actions(self, run: Any) -> None:
        """Handle any required actions from the assistant"""
        if run.required_action.type == "submit_tool_outputs":
            tool_outputs = []
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                output = self._execute_tool_call(tool_call)
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": json.dumps(output)
                })

            client.beta.threads.runs.submit_tool_outputs(
                thread_id=self.thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

    def _execute_tool_call(self, tool_call: Any) -> Dict[str, Any]:
        """Execute a tool call and return the result"""
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if function_name == "analyzePrompt":
            return self._analyze_prompt(arguments["prompt"], arguments.get("context"))
        elif function_name == "generateExample":
            return self._generate_example(arguments["topic"], arguments.get("difficulty", "intermediate"))
        elif function_name == "assessLearning":
            return self._assess_learning(arguments["concept"], arguments["submission"])

        return {"error": "Unknown function"}

    def _analyze_prompt(self, prompt: str, context: str = None) -> Dict[str, Any]:
        """Analyze a prompt and provide feedback"""
        # This would typically include more sophisticated analysis
        analysis = {
            "structure": {
                "clarity": self._rate_clarity(prompt),
                "specificity": self._rate_specificity(prompt),
                "completeness": self._rate_completeness(prompt)
            },
            "suggestions": self._generate_suggestions(prompt),
            "best_practices": self._check_best_practices(prompt),
            "context_analysis": self._analyze_context(prompt, context) if context else None
        }
        return analysis

    def _generate_example(self, topic: str, difficulty: str = "intermediate") -> Dict[str, Any]:
        """Generate an example prompt and response"""
        # This would typically pull from a database of examples or generate dynamically
        return {
            "topic": topic,
            "difficulty": difficulty,
            "example_prompt": f"Here's an example prompt for {topic}...",
            "expected_response": "Example response...",
            "explanation": f"This example demonstrates key concepts in {topic}..."
        }

    def _assess_learning(self, concept: str, submission: str) -> Dict[str, Any]:
        """Assess student understanding of a concept"""
        # This would typically include more sophisticated assessment logic
        return {
            "concept": concept,
            "understanding_level": "intermediate",
            "strengths": ["Clear structure", "Good use of context"],
            "areas_for_improvement": ["Could be more specific", "Consider edge cases"],
            "next_steps": ["Practice with more complex scenarios", "Review best practices"]
        }

    # Helper methods for prompt analysis
    def _rate_clarity(self, prompt: str) -> int:
        """Rate the clarity of a prompt from 1-10"""
        # Add your clarity rating logic here
        return 8

    def _rate_specificity(self, prompt: str) -> int:
        """Rate the specificity of a prompt from 1-10"""
        # Add your specificity rating logic here
        return 7

    def _rate_completeness(self, prompt: str) -> int:
        """Rate the completeness of a prompt from 1-10"""
        # Add your completeness rating logic here
        return 9

    def _generate_suggestions(self, prompt: str) -> List[str]:
        """Generate improvement suggestions for a prompt"""
        # Add your suggestion generation logic here
        return ["Add more context", "Specify output format", "Consider edge cases"]

    def _check_best_practices(self, prompt: str) -> Dict[str, bool]:
        """Check if the prompt follows best practices"""
        # Add your best practices checking logic here
        return {
            "clear_objective": True,
            "specific_format": True,
            "appropriate_context": True
        }

    def _analyze_context(self, prompt: str, context: str) -> Dict[str, Any]:
        """Analyze how well the prompt fits the given context"""
        # Add your context analysis logic here
        return {
            "relevance": "high",
            "completeness": "medium",
            "suggestions": ["Consider adding domain-specific terminology"]
        }

def main():
    """Main function to demonstrate the assistant's capabilities"""
    assistant = PromptEngineeringAssistant()
    
    # Example usage
    print("Starting conversation with Prompt Engineering Assistant...")
    assistant.start_conversation()
    
    # Example interactions
    examples = [
        "Can you help me understand what makes a good prompt?",
        "Analyze this prompt: 'Write a blog post about AI'",
        "Generate an example prompt for sentiment analysis",
        "How can I improve my prompt engineering skills?"
    ]
    
    for example in examples:
        print(f"\nUser: {example}")
        response = assistant.send_message(example)
        print(f"Assistant: {response['content']}")

if __name__ == "__main__":
    main() 