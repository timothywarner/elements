"""
Practical Prompt Engineering Examples
=====================================

This file contains ready-to-use code examples for implementing
prompt engineering and context engineering best practices.

Requirements:
    pip install openai anthropic tiktoken sentence-transformers chromadb

Author: Tim Warner
Last Updated: January 2025
"""

import json
import os
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


# =============================================================================
# Configuration and Setup
# =============================================================================

@dataclass
class LLMConfig:
    """Configuration for LLM API calls"""
    model: str = "gpt-4-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 1.0


class PromptFramework(Enum):
    """Supported prompt frameworks"""
    GOAL = "goal"
    COSTAR = "costar"
    CARE = "care"
    TRACE = "trace"
    RECIPE = "recipe"


# =============================================================================
# Token Management
# =============================================================================

class TokenCounter:
    """Count tokens for different models"""

    def __init__(self, model: str = "gpt-4"):
        try:
            import tiktoken
            self.encoding = tiktoken.encoding_for_model(model)
        except Exception as e:
            print(f"Warning: Could not load tiktoken: {e}")
            self.encoding = None

    def count(self, text: str) -> int:
        """Count tokens in text"""
        if self.encoding:
            return len(self.encoding.encode(text))
        else:
            # Rough approximation
            return len(text) // 4

    def estimate_cost(self, input_tokens: int, output_tokens: int,
                     model: str = "gpt-4-turbo") -> Dict[str, float]:
        """Estimate API cost"""
        pricing = {
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-4o": {"input": 0.005, "output": 0.015},
            "claude-3.5-sonnet": {"input": 0.003, "output": 0.015},
        }

        prices = pricing.get(model, {"input": 0.01, "output": 0.03})

        input_cost = (input_tokens / 1000) * prices["input"]
        output_cost = (output_tokens / 1000) * prices["output"]

        return {
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": input_cost + output_cost,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }


# =============================================================================
# Prompt Templates
# =============================================================================

class PromptTemplate:
    """Reusable prompt templates with variable substitution"""

    def __init__(self, template: str, required_vars: List[str]):
        self.template = template
        self.required_vars = required_vars

    def format(self, **kwargs) -> str:
        """Format template with provided variables"""
        missing = [var for var in self.required_vars if var not in kwargs]
        if missing:
            raise ValueError(f"Missing required variables: {missing}")

        return self.template.format(**kwargs)


# Example templates
TEMPLATES = {
    "code_review": PromptTemplate(
        template="""
        You are an expert code reviewer specializing in {language}.

        Review this code for:
        - Code quality and best practices
        - Potential bugs
        - Security vulnerabilities
        - Performance issues
        - Maintainability

        Code:
        ```{language}
        {code}
        ```

        Provide:
        1. Overall assessment (1-10 score)
        2. Critical issues (must fix)
        3. Recommendations (should fix)
        4. Suggestions (nice to have)

        Format as structured markdown.
        """,
        required_vars=["language", "code"]
    ),

    "data_extraction": PromptTemplate(
        template="""
        Extract structured information from the following text.

        Text:
        {text}

        Extract and return as JSON with this structure:
        {json_schema}

        Rules:
        - Only extract information explicitly stated in the text
        - Use null for missing information
        - Ensure valid JSON output
        - No additional commentary

        JSON:
        """,
        required_vars=["text", "json_schema"]
    ),

    "few_shot_classification": PromptTemplate(
        template="""
        Classify the following text into one of these categories: {categories}

        Examples:

        {examples}

        Now classify this:
        Text: {text}
        Category:
        """,
        required_vars=["categories", "examples", "text"]
    ),
}


# =============================================================================
# Chain-of-Thought Implementations
# =============================================================================

class ChainOfThought:
    """Chain-of-thought prompting utilities"""

    @staticmethod
    def zero_shot(problem: str) -> str:
        """Zero-shot chain-of-thought"""
        return f"""
        Solve this problem step by step.

        Problem: {problem}

        Let's think step by step:
        """

    @staticmethod
    def few_shot(problem: str, examples: List[Dict[str, str]]) -> str:
        """Few-shot chain-of-thought with examples"""
        prompt = "Solve problems using step-by-step reasoning.\n\n"

        for i, ex in enumerate(examples, 1):
            prompt += f"Example {i}:\n"
            prompt += f"Problem: {ex['problem']}\n"
            prompt += f"Reasoning: {ex['reasoning']}\n"
            prompt += f"Answer: {ex['answer']}\n\n"

        prompt += f"Now solve this problem:\n"
        prompt += f"Problem: {problem}\n"
        prompt += f"Reasoning:"

        return prompt

    @staticmethod
    def self_consistency(problem: str, num_paths: int = 3) -> str:
        """Self-consistency CoT"""
        return f"""
        Solve this problem using {num_paths} different reasoning paths.

        Problem: {problem}

        Path 1:
        [Your step-by-step reasoning]
        Answer: [your answer]

        Path 2:
        [Alternative step-by-step reasoning]
        Answer: [your answer]

        Path 3:
        [Another alternative reasoning]
        Answer: [your answer]

        Consistency Check:
        - If all paths agree: Final answer is [answer]
        - If paths disagree: Most likely answer is [answer] because [reasoning]

        Final Answer:
        """


# =============================================================================
# Context Management
# =============================================================================

class ContextManager:
    """Manage context for LLM interactions"""

    def __init__(self, max_tokens: int = 100000):
        self.max_tokens = max_tokens
        self.token_counter = TokenCounter()
        self.context_cache = {}

    def build_layered_context(self,
                             components: Dict[str, str],
                             priority_order: List[str]) -> str:
        """
        Build context with priority layers, fitting within token budget
        """
        context_parts = []
        used_tokens = 0

        for component_name in priority_order:
            if component_name not in components:
                continue

            component = components[component_name]
            component_tokens = self.token_counter.count(component)

            if used_tokens + component_tokens <= self.max_tokens:
                context_parts.append(f"\n# {component_name}\n{component}")
                used_tokens += component_tokens
            else:
                # Try to compress
                compressed = self._compress_to_fit(
                    component,
                    self.max_tokens - used_tokens
                )
                if compressed:
                    context_parts.append(f"\n# {component_name}\n{compressed}")
                break

        return "\n".join(context_parts)

    def _compress_to_fit(self, text: str, target_tokens: int) -> Optional[str]:
        """Compress text to fit token budget"""
        current_tokens = self.token_counter.count(text)

        if current_tokens <= target_tokens:
            return text

        # Simple compression: truncate at sentence boundaries
        sentences = text.split('.')
        compressed = []
        tokens = 0

        for sentence in sentences:
            sentence_tokens = self.token_counter.count(sentence)
            if tokens + sentence_tokens <= target_tokens:
                compressed.append(sentence)
                tokens += sentence_tokens
            else:
                break

        return '.'.join(compressed) + '.' if compressed else None


class ConversationMemory:
    """Manage conversation history with different strategies"""

    def __init__(self, strategy: str = "buffer", max_messages: int = 10):
        self.strategy = strategy
        self.max_messages = max_messages
        self.messages = []
        self.summary = ""

    def add_message(self, role: str, content: str):
        """Add a message to conversation history"""
        self.messages.append({"role": role, "content": content})

        if self.strategy == "buffer":
            self._manage_buffer()
        elif self.strategy == "summary":
            self._manage_summary()

    def _manage_buffer(self):
        """Keep only last N messages"""
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def _manage_summary(self):
        """Maintain rolling summary"""
        if len(self.messages) > self.max_messages:
            # In production, use LLM to summarize
            old_messages = self.messages[:-self.max_messages]
            self.summary = self._create_summary(old_messages)
            self.messages = self.messages[-self.max_messages:]

    def _create_summary(self, messages: List[Dict]) -> str:
        """Create summary of messages (placeholder)"""
        # In production, call LLM here
        return f"Summary of {len(messages)} messages"

    def get_context(self) -> str:
        """Get conversation context"""
        context = ""

        if self.summary:
            context += f"Previous conversation summary:\n{self.summary}\n\n"

        context += "Recent conversation:\n"
        for msg in self.messages:
            context += f"{msg['role']}: {msg['content']}\n"

        return context


# =============================================================================
# RAG (Retrieval-Augmented Generation)
# =============================================================================

class SimpleRAG:
    """
    Basic RAG implementation using sentence transformers and ChromaDB

    In production, use more sophisticated embedding models and vector stores.
    """

    def __init__(self, collection_name: str = "knowledge_base"):
        try:
            from sentence_transformers import SentenceTransformer
            import chromadb
            from chromadb.config import Settings

            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

            self.chroma_client = chromadb.Client(Settings(
                anonymized_telemetry=False,
            ))

            self.collection = self.chroma_client.get_or_create_collection(
                name=collection_name
            )

            self.available = True

        except ImportError:
            print("Warning: sentence-transformers or chromadb not installed")
            self.available = False

    def add_documents(self, documents: List[str],
                     metadata: Optional[List[Dict]] = None):
        """Add documents to knowledge base"""
        if not self.available:
            return

        embeddings = self.embedder.encode(documents).tolist()
        ids = [f"doc_{i}" for i in range(len(documents))]

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadata if metadata else [{}] * len(documents)
        )

    def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """Retrieve most relevant documents"""
        if not self.available:
            return []

        query_embedding = self.embedder.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results['documents'][0] if results['documents'] else []

    def build_context(self, query: str, top_k: int = 3) -> str:
        """Build context from retrieved documents"""
        docs = self.retrieve(query, top_k)

        context = "Retrieved information:\n\n"
        for i, doc in enumerate(docs, 1):
            context += f"[Document {i}]\n{doc}\n\n"

        return context


# =============================================================================
# Prompt Frameworks
# =============================================================================

class FrameworkBuilder:
    """Build prompts using standard frameworks"""

    @staticmethod
    def goal(goal: str, output: str, audience: str, length: str) -> str:
        """Microsoft GOAL framework"""
        return f"""
**Goal**: {goal}
**Output**: {output}
**Audience**: {audience}
**Length**: {length}
"""

    @staticmethod
    def costar(context: str, objective: str, style: str,
              tone: str, audience: str, response: str) -> str:
        """COSTAR framework"""
        return f"""
**Context**: {context}
**Objective**: {objective}
**Style**: {style}
**Tone**: {tone}
**Audience**: {audience}
**Response**: {response}
"""

    @staticmethod
    def care(context: str, action: str, result: str, example: str) -> str:
        """CARE framework"""
        return f"""
**Context**: {context}
**Action**: {action}
**Result**: {result}
**Example**: {example}
"""

    @staticmethod
    def recipe(role: str, end_goal: str, context: str,
              instructions: str, parameters: str, examples: str) -> str:
        """RECIPE framework"""
        return f"""
**Role**: {role}
**End Goal**: {end_goal}
**Context**: {context}
**Instructions**: {instructions}
**Parameters**: {parameters}
**Examples**: {examples}
"""


# =============================================================================
# Prompt Optimization
# =============================================================================

class PromptOptimizer:
    """Tools for optimizing prompts"""

    @staticmethod
    def remove_redundancy(text: str) -> str:
        """Remove redundant phrases and excessive whitespace"""
        # Remove excessive whitespace
        text = re.sub(r'\n\n+', '\n\n', text)
        text = re.sub(r'  +', ' ', text)

        # Remove common redundant phrases
        redundant = [
            "as mentioned earlier",
            "as previously stated",
            "in other words",
            "it should be noted that",
            "it is important to note that",
        ]

        for phrase in redundant:
            text = text.replace(phrase, "")

        return text.strip()

    @staticmethod
    def ensure_clarity(prompt: str) -> List[str]:
        """Check prompt for clarity issues"""
        issues = []

        # Check for ambiguous pronouns
        if re.search(r'\bit\b.*\bit\b', prompt, re.IGNORECASE):
            issues.append("Multiple uses of 'it' may be ambiguous")

        # Check for missing action verbs
        if not any(verb in prompt.lower() for verb in
                  ['analyze', 'create', 'generate', 'write', 'extract',
                   'summarize', 'evaluate', 'compare']):
            issues.append("No clear action verb found")

        # Check for output format specification
        if "format" not in prompt.lower() and "structure" not in prompt.lower():
            issues.append("Consider specifying output format")

        return issues


# =============================================================================
# Example Usage Functions
# =============================================================================

def example_basic_prompt():
    """Example: Creating a well-structured prompt"""
    template = TEMPLATES["code_review"]

    code_sample = """
def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)
"""

    prompt = template.format(
        language="python",
        code=code_sample
    )

    print("=== Basic Prompt Example ===")
    print(prompt)
    print("\n")


def example_chain_of_thought():
    """Example: Chain-of-thought prompting"""
    problem = "If a store has a 25% off sale and you have a 10% coupon, what's the total discount?"

    cot = ChainOfThought()
    prompt = cot.zero_shot(problem)

    print("=== Chain-of-Thought Example ===")
    print(prompt)
    print("\n")


def example_context_management():
    """Example: Managing context with token limits"""
    manager = ContextManager(max_tokens=1000)

    components = {
        "system_prompt": "You are a helpful coding assistant.",
        "project_context": "Working on an e-commerce platform built with React and Node.js.",
        "user_history": "User previously asked about authentication and database design.",
        "documentation": "API documentation: [lengthy docs here]...",
        "examples": "Example code: [multiple examples]...",
    }

    priority = ["system_prompt", "project_context", "user_history",
                "documentation", "examples"]

    context = manager.build_layered_context(components, priority)

    print("=== Context Management Example ===")
    print(f"Context length: {manager.token_counter.count(context)} tokens")
    print(context[:500] + "...")
    print("\n")


def example_framework_usage():
    """Example: Using prompt frameworks"""
    builder = FrameworkBuilder()

    prompt = builder.goal(
        goal="Create a technical blog post about prompt engineering",
        output="1500-word article with code examples and practical tips",
        audience="Software developers new to LLMs",
        length="1500 words"
    )

    print("=== Framework Usage Example ===")
    print(prompt)
    print("\n")


def example_token_counting():
    """Example: Counting tokens and estimating costs"""
    counter = TokenCounter()

    prompt = "Write a comprehensive guide to prompt engineering with examples."
    input_tokens = counter.count(prompt)

    # Assume 500 token response
    output_tokens = 500

    costs = counter.estimate_cost(input_tokens, output_tokens, "gpt-4-turbo")

    print("=== Token Counting Example ===")
    print(f"Input tokens: {costs['input_tokens']}")
    print(f"Output tokens: {costs['output_tokens']}")
    print(f"Input cost: ${costs['input_cost']:.4f}")
    print(f"Output cost: ${costs['output_cost']:.4f}")
    print(f"Total cost: ${costs['total_cost']:.4f}")
    print("\n")


def example_conversation_memory():
    """Example: Managing conversation history"""
    memory = ConversationMemory(strategy="buffer", max_messages=5)

    # Simulate a conversation
    memory.add_message("user", "What's the weather like?")
    memory.add_message("assistant", "I don't have access to real-time weather data.")
    memory.add_message("user", "Can you help me with Python?")
    memory.add_message("assistant", "Yes! What would you like to know about Python?")

    context = memory.get_context()

    print("=== Conversation Memory Example ===")
    print(context)
    print("\n")


def example_prompt_optimization():
    """Example: Optimizing a prompt"""
    optimizer = PromptOptimizer()

    messy_prompt = """
As mentioned earlier, it should be noted that you should analyze this
code and  look  at  it carefully. As previously stated, it is important
to note that you should check for bugs in it and see if it has any issues.
"""

    optimized = optimizer.remove_redundancy(messy_prompt)
    issues = optimizer.ensure_clarity(optimized)

    print("=== Prompt Optimization Example ===")
    print("Original:")
    print(messy_prompt)
    print("\nOptimized:")
    print(optimized)
    print("\nClarity issues:")
    for issue in issues:
        print(f"  - {issue}")
    print("\n")


# =============================================================================
# Main Demo
# =============================================================================

def main():
    """Run all examples"""
    print("=" * 70)
    print("PROMPT ENGINEERING EXAMPLES")
    print("=" * 70)
    print("\n")

    example_basic_prompt()
    example_chain_of_thought()
    example_context_management()
    example_framework_usage()
    example_token_counting()
    example_conversation_memory()
    example_prompt_optimization()

    print("=" * 70)
    print("For more examples, see the documentation in docs/")
    print("=" * 70)


if __name__ == "__main__":
    main()
