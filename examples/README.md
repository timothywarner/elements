# Prompt Engineering Code Examples

This directory contains practical, ready-to-use code examples for implementing prompt engineering and context engineering best practices.

## Files

### prompt_engineering_examples.py

Complete Python implementation featuring:

- **Token Management**: Count tokens and estimate API costs
- **Prompt Templates**: Reusable templates with variable substitution
- **Chain-of-Thought**: Zero-shot, few-shot, and self-consistency implementations
- **Context Management**: Layered context building with token budget management
- **Conversation Memory**: Buffer and summary-based conversation history
- **RAG**: Basic Retrieval-Augmented Generation implementation
- **Prompt Frameworks**: GOAL, COSTAR, CARE, and RECIPE builders
- **Optimization Tools**: Prompt cleanup and clarity checking

## Quick Start

### Installation

```bash
# Core dependencies
pip install openai anthropic tiktoken

# Optional: For RAG examples
pip install sentence-transformers chromadb
```

### Basic Usage

```python
from prompt_engineering_examples import PromptTemplate, TokenCounter, FrameworkBuilder

# Count tokens
counter = TokenCounter()
tokens = counter.count("Your prompt here")
print(f"Token count: {tokens}")

# Use a template
template = TEMPLATES["code_review"]
prompt = template.format(language="python", code="def hello(): pass")

# Use a framework
builder = FrameworkBuilder()
prompt = builder.goal(
    goal="Write a blog post",
    output="1500-word article",
    audience="Developers",
    length="1500 words"
)
```

### Running Examples

```bash
# Run all examples
python prompt_engineering_examples.py
```

## Examples Included

### 1. Basic Prompt Creation

```python
example_basic_prompt()
```

Shows how to use prompt templates for consistent, reusable prompts.

### 2. Chain-of-Thought Prompting

```python
example_chain_of_thought()
```

Demonstrates zero-shot and few-shot chain-of-thought techniques.

### 3. Context Management

```python
example_context_management()
```

Shows how to build layered context within token budgets.

### 4. Framework Usage

```python
example_framework_usage()
```

Examples of GOAL, COSTAR, CARE, and RECIPE frameworks.

### 5. Token Counting & Cost Estimation

```python
example_token_counting()
```

Calculate token usage and estimate API costs.

### 6. Conversation Memory

```python
example_conversation_memory()
```

Manage conversation history with different strategies.

### 7. Prompt Optimization

```python
example_prompt_optimization()
```

Clean up and optimize prompts for clarity and efficiency.

## Advanced Usage

### Custom RAG Implementation

```python
from prompt_engineering_examples import SimpleRAG

# Initialize RAG system
rag = SimpleRAG(collection_name="my_knowledge_base")

# Add documents
documents = [
    "Python is a high-level programming language.",
    "JavaScript is used for web development.",
    "Go is known for its concurrency features.",
]
rag.add_documents(documents)

# Retrieve relevant documents
query = "Tell me about Python"
docs = rag.retrieve(query, top_k=2)

# Build context with retrieved docs
context = rag.build_context(query, top_k=2)
```

### Context Manager with Priority

```python
from prompt_engineering_examples import ContextManager

manager = ContextManager(max_tokens=5000)

components = {
    "system": "You are a helpful assistant",
    "context": "Project background information...",
    "history": "Previous conversation...",
    "docs": "Relevant documentation...",
}

# Build context with priority order
context = manager.build_layered_context(
    components,
    priority_order=["system", "context", "history", "docs"]
)
```

### Conversation Memory Strategies

```python
from prompt_engineering_examples import ConversationMemory

# Buffer strategy (keep last N messages)
buffer_memory = ConversationMemory(strategy="buffer", max_messages=10)

# Summary strategy (summarize old messages)
summary_memory = ConversationMemory(strategy="summary", max_messages=5)

# Add messages
buffer_memory.add_message("user", "Hello!")
buffer_memory.add_message("assistant", "Hi! How can I help?")

# Get conversation context
context = buffer_memory.get_context()
```

## Integration with LLM APIs

### OpenAI Example

```python
import openai
from prompt_engineering_examples import PromptTemplate, TokenCounter

# Count tokens before API call
counter = TokenCounter(model="gpt-4")
prompt = "Explain prompt engineering"
tokens = counter.count(prompt)

# Make API call
response = openai.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
)

# Estimate cost
output_tokens = counter.count(response.choices[0].message.content)
cost = counter.estimate_cost(tokens, output_tokens, "gpt-4-turbo")
print(f"Total cost: ${cost['total_cost']:.4f}")
```

### Anthropic Claude Example

```python
import anthropic
from prompt_engineering_examples import ContextManager

client = anthropic.Anthropic(api_key="your-api-key")

# Build context
manager = ContextManager()
context = manager.build_layered_context(
    {"system": "You are Claude", "task": "Write code"},
    ["system", "task"]
)

# Make API call
message = client.messages.create(
    model="claude-3-5-sonnet-20250101",
    max_tokens=1024,
    messages=[{"role": "user", "content": context}]
)
```

## Best Practices

1. **Always count tokens** before making API calls to avoid surprises
2. **Use templates** for consistency and maintainability
3. **Version your prompts** like code
4. **Test with diverse inputs** to catch edge cases
5. **Monitor costs** in production
6. **Cache responses** when using deterministic settings (temperature=0)

## Common Patterns

### Pattern 1: Extract Structured Data

```python
template = TEMPLATES["data_extraction"]
prompt = template.format(
    text="John Smith works at Acme Corp as a Software Engineer.",
    json_schema='{"name": "", "company": "", "title": ""}'
)
```

### Pattern 2: Few-Shot Classification

```python
template = TEMPLATES["few_shot_classification"]
prompt = template.format(
    categories="positive, negative, neutral",
    examples="Example 1: 'Great product!' -> positive\nExample 2: 'Terrible!' -> negative",
    text="It's okay"
)
```

### Pattern 3: Chain-of-Thought for Math

```python
cot = ChainOfThought()
prompt = cot.zero_shot("If I buy 3 items at $15 each with 20% off, what's the total?")
```

## Troubleshooting

### "Module not found" errors

Install missing dependencies:
```bash
pip install -r requirements.txt
```

### Token counting not working

Make sure tiktoken is installed:
```bash
pip install tiktoken
```

### RAG examples not working

Install optional dependencies:
```bash
pip install sentence-transformers chromadb
```

## Resources

- [Main Documentation](../docs/)
- [Prompt Engineering Best Practices](../docs/Prompt-Engineering-Best-Practices-2025.md)
- [Context Engineering Guide](../docs/Context-Engineering-Guide-2025.md)
- [Advanced Techniques](../docs/Advanced-Prompting-Techniques-2025.md)

## Contributing

To add new examples:

1. Follow the existing code style
2. Add docstrings to all functions
3. Include usage examples
4. Update this README

---

*Last updated: January 2025*
