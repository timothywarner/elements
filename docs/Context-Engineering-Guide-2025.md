# Context Engineering for LLMs: Complete Guide 2025

*Master the art of context management for optimal LLM performance*

---

## Table of Contents

1. [Introduction to Context Engineering](#introduction-to-context-engineering)
2. [Understanding Context Windows](#understanding-context-windows)
3. [Context Architecture Patterns](#context-architecture-patterns)
4. [Context Optimization Techniques](#context-optimization-techniques)
5. [Retrieval-Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
6. [Memory and State Management](#memory-and-state-management)
7. [Context Injection Strategies](#context-injection-strategies)
8. [Production Patterns](#production-patterns)
9. [Cost Optimization](#cost-optimization)
10. [Troubleshooting](#troubleshooting)

---

## Introduction to Context Engineering

### What is Context Engineering?

Context engineering is the practice of strategically managing, structuring, and optimizing the information provided to Large Language Models to maximize performance, accuracy, and cost-efficiency.

### Why Context Engineering Matters

**The Challenge**: LLMs are stateless and have limited context windows. Every interaction requires:
- Relevant background information
- Task instructions
- Previous conversation history (if applicable)
- Domain-specific knowledge
- Examples and formatting guidelines

**The Impact**:
- **Accuracy**: Better context → Better outputs
- **Cost**: Efficient context → Lower token costs
- **Latency**: Optimized context → Faster responses
- **Reliability**: Structured context → More consistent results

### Context vs. Prompts

| Aspect | Prompt | Context |
|--------|--------|---------|
| **Purpose** | Instructs what to do | Provides information to work with |
| **Frequency** | Changes per request | Often reused or templated |
| **Size** | Typically smaller | Can be very large |
| **Optimization** | Clarity and specificity | Relevance and efficiency |

---

## Understanding Context Windows

### Current Model Capabilities (2025)

| Model | Context Window | Effective Usage | Notes |
|-------|----------------|-----------------|-------|
| GPT-4 Turbo | 128K tokens | ~100K tokens | Better performance in first/last 20% |
| GPT-4o | 128K tokens | ~100K tokens | Optimized for speed |
| Claude 3.5 Sonnet | 200K tokens | ~180K tokens | Strong throughout window |
| Claude 3 Opus | 200K tokens | ~180K tokens | Best for long documents |
| Gemini 1.5 Pro | 2M tokens | ~1.5M tokens | Exceptional for massive context |
| Gemini 1.5 Flash | 1M tokens | ~800K tokens | Fast, good for medium context |
| Llama 3.1 405B | 128K tokens | ~100K tokens | Open source option |

**Key Insight**: Models often perform best with information placed at the beginning or end of the context window (the "lost in the middle" problem).

### Token Counting

Understanding token usage is critical:

```python
import tiktoken

def count_tokens(text, model="gpt-4"):
    """
    Count tokens for a given text and model
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Example
text = "Your context here"
tokens = count_tokens(text)
print(f"Token count: {tokens}")
print(f"Estimated cost (GPT-4): ${tokens * 0.00003:.4f}")
```

**Rules of Thumb**:
- 1 token ≈ 4 characters (English)
- 1 token ≈ 0.75 words (English)
- Code is more token-dense than prose
- Special characters and formatting add tokens

---

## Context Architecture Patterns

### 1. Direct Context Injection

**Use case**: Small, static context that fits easily in the window

**Pattern**:
```
System: You are a customer service agent for TechCorp.

Company Context:
- Founded in 2010
- Specializes in cloud storage solutions
- 10M+ users worldwide
- 24/7 support available

Policies:
- 30-day money-back guarantee
- Free tier: 5GB storage
- Pro tier: 100GB storage, $9.99/month
- Enterprise: Custom pricing

User Question: {user_input}

Response:
```

**Pros**: Simple, fast, predictable
**Cons**: Doesn't scale, expensive for large context, no dynamic updates

### 2. Hierarchical Context

**Use case**: Multi-level information that needs organization

**Pattern**:
```
# System Context (Always included)
Role: Senior software architect
Primary goal: Design scalable systems

# Domain Context (Project-specific)
Project: E-commerce platform redesign
Stack: React, Node.js, PostgreSQL, AWS
Scale: 1M daily active users

# Task Context (Request-specific)
Current task: Database schema design
Focus: Order management system
Constraints: Must support 10K orders/minute

# Reference Context (As needed)
Existing schema: [schema_dump]
Related services: [service_list]

# Input
User request: {request}
```

**Pros**: Organized, clear hierarchy, easy to modify sections
**Cons**: Requires careful structure maintenance

### 3. Layered Context with Prioritization

**Use case**: When you have more context than fits in the window

**Pattern**:
```python
def build_layered_context(request, max_tokens=100000):
    """
    Build context with priority layers
    """
    context_layers = {
        "critical": {  # Always include
            "system_prompt": get_system_prompt(),
            "task_definition": get_task_definition(),
        },
        "high_priority": {  # Include if space available
            "recent_conversation": get_recent_history(turns=5),
            "user_preferences": get_user_preferences(),
        },
        "medium_priority": {  # Include if space available
            "relevant_docs": get_relevant_docs(request, top_k=3),
            "examples": get_few_shot_examples(n=2),
        },
        "low_priority": {  # Include if space available
            "full_history": get_full_history(),
            "extended_docs": get_relevant_docs(request, top_k=10),
        }
    }

    # Build context from highest to lowest priority
    context = ""
    remaining_tokens = max_tokens

    for priority in ["critical", "high_priority", "medium_priority", "low_priority"]:
        for key, value in context_layers[priority].items():
            tokens = count_tokens(value)
            if tokens <= remaining_tokens:
                context += f"\n# {key}\n{value}\n"
                remaining_tokens -= tokens
            else:
                break

    return context
```

**Pros**: Makes best use of available context, adapts to token limits
**Cons**: More complex to implement and debug

### 4. Rolling Window Context

**Use case**: Long conversations that exceed context limits

**Pattern**:
```python
class RollingContextManager:
    def __init__(self, max_tokens=100000):
        self.max_tokens = max_tokens
        self.system_prompt = ""  # Always kept
        self.messages = []

    def add_message(self, role, content):
        """
        Add message and trim if necessary
        """
        self.messages.append({"role": role, "content": content})

        # Calculate total tokens
        total_tokens = count_tokens(self.system_prompt)
        for msg in self.messages:
            total_tokens += count_tokens(msg["content"])

        # Trim oldest messages if over limit
        while total_tokens > self.max_tokens and len(self.messages) > 2:
            # Keep last message and remove oldest
            removed = self.messages.pop(0)
            total_tokens -= count_tokens(removed["content"])

    def get_context(self):
        """
        Return current context
        """
        return {
            "system": self.system_prompt,
            "messages": self.messages
        }
```

**Pros**: Handles unlimited conversation length
**Cons**: Loses older context, may lose important information

### 5. Summarization-Based Context

**Use case**: Very long conversations or documents

**Pattern**:
```python
class SummarizationContextManager:
    def __init__(self):
        self.system_prompt = ""
        self.summary = ""  # Rolling summary of old context
        self.recent_messages = []  # Detailed recent messages

    def add_message(self, role, content):
        """
        Add message and maintain summary
        """
        self.recent_messages.append({"role": role, "content": content})

        # If recent messages exceed threshold, summarize older ones
        if len(self.recent_messages) > 10:
            # Get oldest messages to summarize
            to_summarize = self.recent_messages[:5]
            self.recent_messages = self.recent_messages[5:]

            # Generate summary
            new_summary = self.summarize_messages(to_summarize)

            # Update rolling summary
            if self.summary:
                self.summary = self.combine_summaries(
                    self.summary,
                    new_summary
                )
            else:
                self.summary = new_summary

    def summarize_messages(self, messages):
        """
        Use LLM to summarize messages
        """
        prompt = f"""
        Summarize the key points from this conversation segment:

        {messages}

        Focus on:
        - Important decisions made
        - Facts established
        - User preferences expressed
        - Unresolved issues

        Summary (2-3 sentences):
        """
        return call_llm(prompt)

    def get_context(self):
        """
        Return context with summary + recent messages
        """
        context = self.system_prompt + "\n\n"

        if self.summary:
            context += f"Previous conversation summary:\n{self.summary}\n\n"

        context += "Recent conversation:\n"
        for msg in self.recent_messages:
            context += f"{msg['role']}: {msg['content']}\n"

        return context
```

**Pros**: Handles unlimited conversation, maintains important context
**Cons**: Summarization can lose details, adds latency and cost

---

## Context Optimization Techniques

### 1. Semantic Compression

Remove redundancy while preserving meaning:

**Before**:
```
The customer service representative should be polite, courteous, and
friendly when interacting with customers. They should be helpful and
supportive. They need to be understanding and empathetic to customer
concerns and issues.
```

**After**:
```
Customer service guidelines:
- Be polite and friendly
- Show empathy
- Provide helpful support
```

**Savings**: ~40% tokens with same meaning

### 2. Structured Data Formats

Use efficient formats for data:

**Inefficient (Prose)**:
```
The product is called "SuperWidget Pro" and it costs $99.99. It comes
in three colors: red, blue, and green. The dimensions are 10 inches
by 5 inches by 2 inches. It weighs 1.5 pounds.
```
Tokens: ~45

**Efficient (Structured)**:
```yaml
product:
  name: SuperWidget Pro
  price: 99.99
  colors: [red, blue, green]
  dimensions: [10, 5, 2]  # inches (L x W x H)
  weight: 1.5  # pounds
```
Tokens: ~30 (33% savings)

**Most Efficient (JSON)**:
```json
{"name":"SuperWidget Pro","price":99.99,"colors":["red","blue","green"],"dim":[10,5,2],"weight":1.5}
```
Tokens: ~25 (44% savings)

### 3. Context Deduplication

Remove repeated information:

```python
def deduplicate_context(context_sections):
    """
    Remove duplicate information across context sections
    """
    seen_content = set()
    deduplicated = []

    for section in context_sections:
        # Create hash of normalized content
        normalized = normalize_text(section)
        content_hash = hash(normalized)

        if content_hash not in seen_content:
            seen_content.add(content_hash)
            deduplicated.append(section)

    return deduplicated
```

### 4. Relevance Filtering

Only include contextually relevant information:

```python
def filter_by_relevance(query, context_candidates, threshold=0.7):
    """
    Filter context by semantic relevance to query
    """
    from sentence_transformers import SentenceTransformer, util

    model = SentenceTransformer('all-MiniLM-L6-v2')

    query_embedding = model.encode(query)
    context_embeddings = model.encode(context_candidates)

    # Calculate similarities
    similarities = util.cos_sim(query_embedding, context_embeddings)[0]

    # Filter by threshold
    relevant_context = [
        context_candidates[i]
        for i, score in enumerate(similarities)
        if score >= threshold
    ]

    return relevant_context
```

### 5. Dynamic Context Loading

Load context based on the request:

```python
class DynamicContextLoader:
    def __init__(self):
        self.context_sources = {
            "product_info": self.load_product_info,
            "user_history": self.load_user_history,
            "documentation": self.load_docs,
            "policies": self.load_policies,
        }

    def build_context(self, request):
        """
        Analyze request and load only relevant context
        """
        # Classify what context is needed
        needed_context = self.classify_context_needs(request)

        # Load only needed context
        context_parts = []
        for context_type in needed_context:
            loader = self.context_sources[context_type]
            context_parts.append(loader(request))

        return "\n\n".join(context_parts)

    def classify_context_needs(self, request):
        """
        Determine which context is needed for this request
        """
        # Simple keyword-based classification
        # In production, use ML classifier
        keywords = {
            "product_info": ["product", "feature", "specification"],
            "user_history": ["my order", "my account", "previous"],
            "documentation": ["how to", "guide", "tutorial"],
            "policies": ["refund", "return", "policy", "terms"],
        }

        needed = []
        request_lower = request.lower()

        for context_type, keyword_list in keywords.items():
            if any(kw in request_lower for kw in keyword_list):
                needed.append(context_type)

        # Always include basics if nothing specific matched
        if not needed:
            needed = ["product_info"]

        return needed
```

---

## Retrieval-Augmented Generation (RAG)

### RAG Architecture

**Traditional Approach**: Put all context in the prompt
**RAG Approach**: Retrieve only relevant context on-demand

```
┌─────────────────┐
│  User Query     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│  Embedding      │────▶│  Vector Store    │
│  Generation     │     │  (ChromaDB/Pinecone)│
└─────────────────┘     └────────┬─────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  Top-K Relevant │
                        │  Documents      │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  Build Context  │
                        │  with Retrieved │
                        │  Docs           │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  LLM Generation │
                        │  with Context   │
                        └─────────────────┘
```

### Implementing Basic RAG

```python
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

class RAGSystem:
    def __init__(self):
        # Initialize embedding model
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

        # Initialize vector store
        self.chroma_client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))

        self.collection = self.chroma_client.get_or_create_collection(
            name="knowledge_base"
        )

    def add_documents(self, documents, metadata=None):
        """
        Add documents to the knowledge base
        """
        # Generate embeddings
        embeddings = self.embedder.encode(documents).tolist()

        # Add to vector store
        ids = [f"doc_{i}" for i in range(len(documents))]
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadata if metadata else [{}] * len(documents)
        )

    def retrieve(self, query, top_k=3):
        """
        Retrieve most relevant documents for a query
        """
        # Generate query embedding
        query_embedding = self.embedder.encode(query).tolist()

        # Search vector store
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results['documents'][0]

    def generate_with_context(self, query, top_k=3):
        """
        Generate response using retrieved context
        """
        # Retrieve relevant documents
        relevant_docs = self.retrieve(query, top_k)

        # Build context
        context = "\n\n".join([
            f"Document {i+1}:\n{doc}"
            for i, doc in enumerate(relevant_docs)
        ])

        # Build prompt with context
        prompt = f"""
        Answer the question using the following context. If the answer
        is not in the context, say "I don't have enough information."

        Context:
        {context}

        Question: {query}

        Answer:
        """

        # Generate response
        response = call_llm(prompt)
        return response, relevant_docs

# Usage
rag = RAGSystem()

# Add knowledge base
documents = [
    "Our return policy allows returns within 30 days of purchase.",
    "Shipping is free for orders over $50.",
    "We offer 24/7 customer support via chat and email.",
]
rag.add_documents(documents)

# Query with retrieval
answer, sources = rag.generate_with_context("What is your return policy?")
print(f"Answer: {answer}")
print(f"Sources: {sources}")
```

### Advanced RAG Patterns

#### 1. Hybrid Search (Keyword + Semantic)

```python
def hybrid_search(query, top_k=5):
    """
    Combine keyword and semantic search
    """
    # Semantic search
    semantic_results = semantic_search(query, top_k=top_k)

    # Keyword search (BM25)
    keyword_results = keyword_search(query, top_k=top_k)

    # Combine and re-rank
    combined = {}
    for doc, score in semantic_results:
        combined[doc] = score * 0.7  # Weight semantic higher

    for doc, score in keyword_results:
        if doc in combined:
            combined[doc] += score * 0.3
        else:
            combined[doc] = score * 0.3

    # Sort by combined score
    ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked[:top_k]]
```

#### 2. Re-ranking Retrieved Documents

```python
from sentence_transformers import CrossEncoder

def rerank_documents(query, documents, top_k=3):
    """
    Re-rank retrieved documents using cross-encoder
    """
    # Initialize re-ranker
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')

    # Create query-document pairs
    pairs = [[query, doc] for doc in documents]

    # Score pairs
    scores = reranker.predict(pairs)

    # Sort by score
    doc_scores = list(zip(documents, scores))
    doc_scores.sort(key=lambda x: x[1], reverse=True)

    return [doc for doc, score in doc_scores[:top_k]]
```

#### 3. Hierarchical Retrieval

```python
class HierarchicalRAG:
    """
    Two-stage retrieval: coarse then fine
    """

    def retrieve(self, query, top_k=3):
        # Stage 1: Retrieve relevant chapters/sections
        relevant_sections = self.retrieve_sections(query, top_k=10)

        # Stage 2: Retrieve specific passages from those sections
        relevant_passages = []
        for section in relevant_sections:
            passages = self.retrieve_from_section(query, section, top_k=2)
            relevant_passages.extend(passages)

        # Re-rank all passages
        final_passages = self.rerank(query, relevant_passages, top_k=top_k)

        return final_passages
```

#### 4. Query Expansion

```python
def expand_query(original_query):
    """
    Expand query with synonyms and related terms
    """
    expansion_prompt = f"""
    Generate 3 alternative phrasings of this query that might help
    find relevant information:

    Original: {original_query}

    Alternatives (one per line):
    """

    alternatives = call_llm(expansion_prompt).strip().split('\n')

    # Search with all variations
    all_results = []
    for query in [original_query] + alternatives:
        results = search(query, top_k=3)
        all_results.extend(results)

    # Deduplicate and re-rank
    unique_results = deduplicate(all_results)
    return rerank(original_query, unique_results)
```

---

## Memory and State Management

### Conversation Memory Patterns

#### 1. Buffer Memory (Simple)

```python
class BufferMemory:
    """
    Keep last N messages in memory
    """
    def __init__(self, max_messages=10):
        self.messages = []
        self.max_messages = max_messages

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def get_context(self):
        return "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in self.messages
        ])
```

#### 2. Summary Memory

```python
class SummaryMemory:
    """
    Maintain a running summary of conversation
    """
    def __init__(self):
        self.summary = ""
        self.recent_messages = []

    def add(self, role, content):
        self.recent_messages.append({"role": role, "content": content})

        if len(self.recent_messages) >= 6:
            # Summarize older messages
            self.update_summary()
            self.recent_messages = self.recent_messages[-2:]

    def update_summary(self):
        messages_text = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in self.recent_messages[:-2]
        ])

        prompt = f"""
        Update the conversation summary:

        Current summary: {self.summary}

        New messages:
        {messages_text}

        Updated summary (key facts and decisions):
        """

        self.summary = call_llm(prompt)

    def get_context(self):
        context = ""
        if self.summary:
            context += f"Summary: {self.summary}\n\n"

        context += "Recent conversation:\n"
        context += "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in self.recent_messages
        ])

        return context
```

#### 3. Entity Memory

```python
class EntityMemory:
    """
    Track entities (people, products, etc.) mentioned in conversation
    """
    def __init__(self):
        self.entities = {}  # {entity_name: [facts]}

    def extract_entities(self, text):
        """
        Extract entities and facts from text
        """
        prompt = f"""
        Extract entities and facts from this text:

        Text: {text}

        Return as JSON:
        {{
            "entity_name": ["fact1", "fact2"]
        }}
        """

        return json.loads(call_llm(prompt))

    def add(self, role, content):
        # Extract entities from message
        entities = self.extract_entities(content)

        # Update entity memory
        for entity, facts in entities.items():
            if entity in self.entities:
                self.entities[entity].extend(facts)
            else:
                self.entities[entity] = facts

    def get_context(self, relevant_entities=None):
        """
        Get entity context (optionally filtered)
        """
        if relevant_entities:
            entities = {
                k: v for k, v in self.entities.items()
                if k in relevant_entities
            }
        else:
            entities = self.entities

        context = "Known facts:\n"
        for entity, facts in entities.items():
            context += f"\n{entity}:\n"
            for fact in facts:
                context += f"  - {fact}\n"

        return context
```

---

## Context Injection Strategies

### 1. Position Matters

Research shows models are better at using information at the start and end of context:

```python
def optimal_context_ordering(
    system_prompt,
    task_instructions,
    context_docs,
    user_query
):
    """
    Order context for optimal performance
    """
    # Priority 1: System prompt (beginning)
    context = f"{system_prompt}\n\n"

    # Priority 2: Task instructions (beginning)
    context += f"{task_instructions}\n\n"

    # Priority 3: Most relevant docs (beginning)
    context += f"Most relevant information:\n{context_docs[0]}\n\n"

    # Priority 4: Additional docs (middle - less important)
    if len(context_docs) > 1:
        context += f"Additional context:\n"
        for doc in context_docs[1:-1]:
            context += f"{doc}\n\n"

    # Priority 5: Second most relevant doc (near end)
    if len(context_docs) > 1:
        context += f"Also important:\n{context_docs[-1]}\n\n"

    # Priority 6: User query (end)
    context += f"Query: {user_query}\n\nResponse:"

    return context
```

### 2. XML/Tag-Based Structure

Help models parse context more effectively:

```python
def structured_context(user_query, background, examples, constraints):
    """
    Use XML-style tags for clear context structure
    """
    return f"""
<system>
You are a helpful assistant specialized in technical writing.
</system>

<background>
{background}
</background>

<examples>
{examples}
</examples>

<constraints>
{constraints}
</constraints>

<query>
{user_query}
</query>

<response>
[Your response here, following the constraints and examples]
</response>
"""
```

### 3. Metadata Injection

Include metadata to help the model understand context relevance:

```python
def context_with_metadata(query, retrieved_docs):
    """
    Include metadata about each context piece
    """
    context = "Retrieved information:\n\n"

    for i, doc in enumerate(retrieved_docs):
        context += f"""
Document {i+1}:
Source: {doc['source']}
Relevance Score: {doc['score']:.2f}
Last Updated: {doc['updated_at']}
Content:
{doc['content']}

---
"""

    context += f"\nQuestion: {query}\n\nAnswer (cite document numbers):"
    return context
```

---

## Production Patterns

### 1. Context Caching

Cache expensive context that doesn't change:

```python
from functools import lru_cache
import hashlib

class ContextCache:
    def __init__(self):
        self.cache = {}

    def get_cached_context(self, context_id):
        """
        Retrieve cached context
        """
        return self.cache.get(context_id)

    def cache_context(self, context_id, context_data):
        """
        Cache context for reuse
        """
        self.cache[context_id] = {
            "data": context_data,
            "timestamp": time.time()
        }

    def build_context_with_cache(self, static_parts, dynamic_parts):
        """
        Combine cached static context with dynamic parts
        """
        # Hash static parts for cache key
        static_hash = hashlib.md5(
            json.dumps(static_parts).encode()
        ).hexdigest()

        # Check cache
        cached = self.get_cached_context(static_hash)

        if cached:
            static_context = cached["data"]
        else:
            static_context = self.build_static_context(static_parts)
            self.cache_context(static_hash, static_context)

        # Build dynamic context fresh
        dynamic_context = self.build_dynamic_context(dynamic_parts)

        return static_context + "\n\n" + dynamic_context
```

### 2. Context Streaming

Stream context for very large documents:

```python
def stream_context_processing(large_document, chunk_size=2000):
    """
    Process large documents in chunks
    """
    chunks = split_into_chunks(large_document, chunk_size)
    results = []

    for i, chunk in enumerate(chunks):
        prompt = f"""
        This is part {i+1} of {len(chunks)} of a document.

        Previous findings: {results[-1] if results else "None"}

        Current chunk:
        {chunk}

        Extract key information from this chunk:
        """

        result = call_llm(prompt)
        results.append(result)

    # Final synthesis
    synthesis_prompt = f"""
    Synthesize these partial analyses into a complete summary:

    {json.dumps(results, indent=2)}

    Complete summary:
    """

    return call_llm(synthesis_prompt)
```

### 3. Adaptive Context Sizing

Adjust context based on token budget:

```python
class AdaptiveContextBuilder:
    def __init__(self, max_tokens=100000):
        self.max_tokens = max_tokens

    def build(self, components, priority_order):
        """
        Build context adaptively within token budget
        """
        context_parts = []
        used_tokens = 0

        for component_name in priority_order:
            component = components[component_name]
            component_tokens = count_tokens(component)

            if used_tokens + component_tokens <= self.max_tokens:
                context_parts.append(component)
                used_tokens += component_tokens
            else:
                # Component doesn't fit, try to compress it
                compressed = self.compress_component(
                    component,
                    target_tokens=self.max_tokens - used_tokens
                )

                if compressed:
                    context_parts.append(compressed)
                    used_tokens += count_tokens(compressed)

                break  # No more room

        return "\n\n".join(context_parts)

    def compress_component(self, component, target_tokens):
        """
        Compress component to fit token budget
        """
        if count_tokens(component) <= target_tokens:
            return component

        # Use LLM to compress
        prompt = f"""
        Compress the following text to approximately {target_tokens} tokens
        while preserving key information:

        {component}

        Compressed version:
        """

        return call_llm(prompt)
```

---

## Cost Optimization

### Token Cost Analysis

```python
class TokenCostAnalyzer:
    """
    Analyze and optimize token costs
    """

    PRICING = {  # Cost per 1K tokens (as of 2025)
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "claude-3.5-sonnet": {"input": 0.003, "output": 0.015},
        "gemini-1.5-pro": {"input": 0.00125, "output": 0.005},
    }

    def calculate_cost(self, input_tokens, output_tokens, model):
        """
        Calculate cost for a request
        """
        pricing = self.PRICING.get(model, {"input": 0, "output": 0})

        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]

        return {
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": input_cost + output_cost
        }

    def analyze_context_efficiency(self, context):
        """
        Find inefficiencies in context
        """
        issues = []

        # Check for repetition
        if has_repetition(context):
            issues.append("Contains repeated information")

        # Check for low-density content
        if average_information_density(context) < 0.5:
            issues.append("Low information density - consider compression")

        # Check for unnecessary formatting
        if excessive_whitespace(context):
            issues.append("Excessive whitespace")

        return issues

    def optimize_context(self, context):
        """
        Apply automatic optimizations
        """
        # Remove excessive whitespace
        optimized = re.sub(r'\n\n+', '\n\n', context)

        # Remove redundant phrases
        redundant_phrases = [
            "as mentioned earlier",
            "as previously stated",
            "in other words",
        ]
        for phrase in redundant_phrases:
            optimized = optimized.replace(phrase, "")

        # Compress data structures
        optimized = compress_data_structures(optimized)

        return optimized
```

### Cost-Effective Context Strategies

```python
# Strategy 1: Context Deduplication
def deduplicate_context_sections(sections):
    """
    Remove duplicate information across sections
    """
    unique_sentences = set()
    deduplicated_sections = []

    for section in sections:
        sentences = section.split('.')
        unique_in_section = []

        for sentence in sentences:
            normalized = sentence.strip().lower()
            if normalized and normalized not in unique_sentences:
                unique_sentences.add(normalized)
                unique_in_section.append(sentence)

        if unique_in_section:
            deduplicated_sections.append('.'.join(unique_in_section))

    return deduplicated_sections

# Strategy 2: Smart Truncation
def smart_truncate(text, max_tokens):
    """
    Truncate text intelligently at sentence boundaries
    """
    sentences = text.split('.')
    truncated = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = count_tokens(sentence)
        if current_tokens + sentence_tokens <= max_tokens:
            truncated.append(sentence)
            current_tokens += sentence_tokens
        else:
            break

    return '.'.join(truncated) + '.'

# Strategy 3: Selective Detail
def selective_detail(content, query, detail_level='medium'):
    """
    Adjust detail level based on relevance to query
    """
    detail_settings = {
        'low': {'max_tokens': 500, 'top_k': 2},
        'medium': {'max_tokens': 2000, 'top_k': 5},
        'high': {'max_tokens': 5000, 'top_k': 10},
    }

    settings = detail_settings[detail_level]

    # Extract most relevant sections
    relevant_sections = extract_relevant(
        query,
        content,
        top_k=settings['top_k']
    )

    # Truncate to token limit
    return smart_truncate(
        '\n\n'.join(relevant_sections),
        settings['max_tokens']
    )
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Lost in the Middle"

**Problem**: Model ignores information in the middle of long context

**Solution**:
```python
def address_lost_in_middle(important_info, other_context, query):
    """
    Place critical information at start AND end
    """
    return f"""
{important_info}  # At the beginning

{other_context}  # Less critical in middle

REMEMBER: {important_info}  # Repeat at end

Question: {query}
"""
```

#### Issue 2: Context Confusion

**Problem**: Model mixes up different pieces of context

**Solution**:
```python
def clear_context_separation(sections):
    """
    Use clear delimiters and labels
    """
    context = ""

    for i, section in enumerate(sections):
        context += f"""
{'='*50}
SECTION {i+1}: {section['title']}
{'='*50}

{section['content']}

"""
    return context
```

#### Issue 3: Outdated Context

**Problem**: Using stale information

**Solution**:
```python
class ContextFreshnessManager:
    def __init__(self, ttl=3600):  # 1 hour default TTL
        self.context_cache = {}
        self.ttl = ttl

    def get_context(self, context_id, refresh_fn):
        """
        Get context with automatic refresh
        """
        cached = self.context_cache.get(context_id)

        if cached and time.time() - cached['timestamp'] < self.ttl:
            return cached['data']

        # Refresh stale context
        fresh_data = refresh_fn()
        self.context_cache[context_id] = {
            'data': fresh_data,
            'timestamp': time.time()
        }

        return fresh_data
```

#### Issue 4: Token Limit Exceeded

**Problem**: Context + prompt exceeds model limit

**Solution**:
```python
def handle_token_overflow(context, prompt, max_tokens=100000):
    """
    Handle context that exceeds token limits
    """
    prompt_tokens = count_tokens(prompt)
    available_tokens = max_tokens - prompt_tokens - 1000  # Buffer for response

    context_tokens = count_tokens(context)

    if context_tokens <= available_tokens:
        return context  # No problem

    # Strategy 1: Summarize context
    summarized = summarize_context(context, target_tokens=available_tokens)

    if count_tokens(summarized) <= available_tokens:
        return summarized

    # Strategy 2: Extract most relevant parts
    relevant = extract_most_relevant(
        context,
        prompt,
        max_tokens=available_tokens
    )

    return relevant
```

---

## Best Practices Summary

### Do's ✓

1. **Structure your context** - Use clear sections and hierarchies
2. **Prioritize information** - Most important first and last
3. **Measure token usage** - Monitor and optimize costs
4. **Cache static context** - Reuse when possible
5. **Use RAG for large knowledge bases** - Don't stuff everything in context
6. **Test with diverse inputs** - Ensure context works for edge cases
7. **Version your context** - Track changes and performance
8. **Validate context freshness** - Update regularly

### Don'ts ✗

1. **Don't dump raw data** - Structure and filter first
2. **Don't repeat information** - Deduplicate across sections
3. **Don't ignore token costs** - Context is expensive
4. **Don't use prose when JSON works** - Be format-efficient
5. **Don't assume position doesn't matter** - It does significantly
6. **Don't skip relevance filtering** - Only include what's needed
7. **Don't forget about the middle** - Information can get lost there
8. **Don't hardcode everything** - Make context dynamic and adaptive

---

## Conclusion

Effective context engineering is crucial for LLM application success. By:

- Understanding context windows and token economics
- Implementing appropriate architecture patterns
- Optimizing for relevance and efficiency
- Using RAG for large knowledge bases
- Managing memory and state effectively
- Following production best practices

You can build LLM applications that are accurate, cost-effective, and scalable.

---

## Resources

- [Anthropic Context Window Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips)
- [OpenAI Token Management](https://platform.openai.com/docs/guides/rate-limits/managing-context)
- [LangChain Memory Types](https://python.langchain.com/docs/modules/memory/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Pinecone RAG Guide](https://www.pinecone.io/learn/retrieval-augmented-generation/)

---

*Last updated: January 2025*
*Version: 1.0*
