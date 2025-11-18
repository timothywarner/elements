# Prompt Engineering Quick Start Guide 2025

*Get started with prompt engineering in 30 minutes*

---

## What is Prompt Engineering?

Prompt engineering is the practice of crafting inputs (prompts) to get the best possible outputs from Large Language Models (LLMs) like GPT-4, Claude, or Gemini.

**Think of it as:** Learning to communicate effectively with an extremely knowledgeable but literal colleague who needs clear instructions.

---

## 5-Minute Fundamentals

### The Basic Formula

```
[CONTEXT] + [INSTRUCTION] + [FORMAT] = Better Output
```

### Bad Prompt ❌
```
Write about AI.
```

### Good Prompt ✓
```
You are a technology journalist writing for a general audience.

Write a 300-word article explaining how AI language models work.

Format:
- Introduction paragraph
- 3 key concepts with examples
- Conclusion
- 8th-grade reading level
```

---

## Your First 10 Prompts

### 1. Be Specific

**Instead of:**
```
Summarize this article.
```

**Try:**
```
Summarize this article in 3 bullet points, focusing on:
1. Main argument
2. Key evidence
3. Conclusions
```

### 2. Assign a Role

**Instead of:**
```
Review my code.
```

**Try:**
```
You are a senior Python developer with expertise in security.
Review this code for:
- Security vulnerabilities
- Best practices violations
- Performance issues

Code:
[your code]
```

### 3. Provide Examples (Few-Shot Learning)

**Instead of:**
```
Convert these to JSON.
```

**Try:**
```
Convert customer feedback to JSON. Examples:

Input: "Great product, fast shipping!"
Output: {"sentiment": "positive", "topic": "shipping"}

Input: "Product broke after 2 days"
Output: {"sentiment": "negative", "topic": "quality"}

Now convert: "Love it but expensive"
Output:
```

### 4. Ask for Step-by-Step Reasoning

**Instead of:**
```
What's 15% of $234?
```

**Try:**
```
Calculate 15% of $234.
Show your work step by step:
1. [step]
2. [step]
Final answer: [result]
```

### 5. Specify Output Format

**Instead of:**
```
List programming languages.
```

**Try:**
```
List 5 popular programming languages.

Format as a markdown table:
| Language | Primary Use | Difficulty |

Include: Python, JavaScript, Java, Go, Rust
```

### 6. Add Constraints

**Instead of:**
```
Write a product description.
```

**Try:**
```
Write a product description for wireless headphones.

Requirements:
- Length: 100-150 words
- Tone: Professional but approachable
- Include: 3 key features, 1 benefit
- Avoid: Technical jargon, superlatives without support
```

### 7. Use Delimiters

**Instead of:**
```
Translate: Hello, how are you? to Spanish
```

**Try:**
```
Translate the following text to Spanish.

Text:
"""
Hello, how are you?
I hope you're having a great day!
"""

Translation:
```

### 8. Request Self-Verification

**Instead of:**
```
Is this code correct? [code]
```

**Try:**
```
Analyze this code:
[code]

Then verify your analysis:
1. Did I identify all potential bugs?
2. Did I miss any edge cases?
3. How confident am I? (1-10)

Final assessment:
```

### 9. Iterate and Refine

**Instead of:**
```
Write a blog post title.
```

**Try:**
```
Generate 5 blog post titles about AI in healthcare.

For each title:
- Make it attention-grabbing
- Include a number or question
- Keep under 60 characters

Then rank them 1-5 with reasoning.
```

### 10. Handle Uncertainty

**Instead of:**
```
What was the population of Beijing in 2023?
```

**Try:**
```
What was the population of Beijing in 2023?

Provide:
- Your answer
- Confidence level (low/medium/high)
- Source of information (training data/calculation/etc.)
- Any important caveats

If you're not confident, say so and explain why.
```

---

## The GOAL Framework

Start with this simple framework for any task:

```
**Goal**: [What you want to achieve]
**Output**: [Specific format/deliverable]
**Audience**: [Who will use this]
**Length**: [Size constraints]
```

**Example:**
```
**Goal**: Create a job posting for a software engineer
**Output**: Complete job posting with requirements and benefits
**Audience**: Experienced developers
**Length**: 300-500 words
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Too Vague
```
Help me with my code.
```

✓ **Fix:**
```
I'm getting a "TypeError: 'NoneType' object is not subscriptable" error
in Python when trying to access a dictionary. Here's my code: [code]
How do I fix this?
```

### ❌ Mistake 2: No Context
```
Fix this bug.
```

✓ **Fix:**
```
I'm building a React app. This component should display user profiles
but shows a blank screen. Expected: profile card. Actual: blank.
Code: [code]
```

### ❌ Mistake 3: Implicit Assumptions
```
Write a function to sort the list.
```

✓ **Fix:**
```
Write a Python function that:
- Input: List of dictionaries with 'name' and 'age' keys
- Output: List sorted by age (ascending)
- Include: Type hints, docstring, error handling for invalid input
```

### ❌ Mistake 4: No Format Specification
```
Analyze this data.
```

✓ **Fix:**
```
Analyze this sales data and provide:

Format:
1. Summary statistics (mean, median, trend)
2. Top 3 insights
3. Recommendations
4. Present as markdown with headers
```

### ❌ Mistake 5: Overloading
```
Analyze this dataset, create visualizations, write a report,
generate SQL queries, build a dashboard, and send an email summary.
```

✓ **Fix:** Break into steps:
```
Step 1: Analyze dataset → Generate summary statistics
Step 2: Based on summary, create 3 key visualizations
[etc.]
```

---

## Quick Reference: Prompt Components

### Essential Components

```
[ROLE]: You are a [expert type]
[CONTEXT]: Background information
[TASK]: What you want done
[FORMAT]: How you want the output
[CONSTRAINTS]: What to include/avoid
[EXAMPLES]: Sample inputs/outputs
```

### Optional Components

```
[TONE]: Professional/casual/technical
[AUDIENCE]: Who will read this
[LENGTH]: Word/character count
[VERIFICATION]: Self-check steps
[REASONING]: Show your work
```

---

## Your First Real-World Task

Let's put it all together:

**Task:** Get help analyzing customer feedback

**Bad Prompt:**
```
Look at these reviews and tell me what people think.
```

**Good Prompt:**
```
You are a customer experience analyst with expertise in sentiment analysis.

Analyze these product reviews and provide actionable insights.

Reviews:
1. "Great product but shipping took forever"
2. "Stopped working after a week, very disappointed"
3. "Love it! Exactly what I needed"
4. "Good quality but overpriced"
5. "Customer service was super helpful when I had issues"

Provide:

1. **Sentiment Distribution**
   - Positive: X%
   - Neutral: X%
   - Negative: X%

2. **Key Themes** (top 3 with frequency)
   - Theme 1: [description]
   - Theme 2: [description]
   - Theme 3: [description]

3. **Priority Issues** (urgent problems to address)
   - Issue 1: [description + severity]
   - Issue 2: [description + severity]

4. **Recommendations** (3 specific actions)
   - Action 1: [what to do]
   - Action 2: [what to do]
   - Action 3: [what to do]

Format as markdown with clear headings.
```

---

## Tips for Different Tasks

### For Code Generation

```
Generate a [language] function that:
- Input: [describe input parameters with types]
- Output: [describe return value with type]
- Does: [specific behavior]
- Handles: [edge cases]
- Includes: [docstrings, type hints, error handling]
- Style: [PEP 8, Google style, etc.]
```

### For Writing

```
Write a [type] about [topic].

Audience: [who reads this]
Tone: [professional/casual/technical]
Length: [word count]
Structure: [outline]
Include: [must-have elements]
Avoid: [things to exclude]
```

### For Analysis

```
Analyze [subject] and identify:
1. [aspect 1]
2. [aspect 2]
3. [aspect 3]

Provide:
- Summary
- Key findings
- Supporting evidence
- Recommendations

Format: [structure specification]
```

### For Data Extraction

```
Extract information from the following text.

Text:
"""
[your text]
"""

Extract and return as JSON:
{
  "field1": "description",
  "field2": "description"
}

Rules:
- Only extract explicitly stated information
- Use null for missing data
- No additional commentary
```

---

## Testing Your Prompts

### Quick Test Checklist

1. **Specificity**: Could someone else understand exactly what you want?
2. **Context**: Have you provided necessary background?
3. **Format**: Is the desired output structure clear?
4. **Examples**: Would examples help clarify expectations?
5. **Constraints**: Are boundaries and limits defined?

### The "New Hire" Test

If you gave this prompt to a smart but uninformed new hire, would they know:
- What to do?
- How to do it?
- What format to use?
- What to avoid?
- How to know if they succeeded?

If no → improve the prompt

---

## Iterating on Prompts

### Version 1 (Too Simple)
```
Write about AI safety.
```

### Version 2 (Adding Structure)
```
Write a 500-word article about AI safety for a general audience.
Include an introduction, 3 main points, and a conclusion.
```

### Version 3 (Adding Specificity)
```
Write a 500-word article about AI safety challenges.

Audience: General public with no AI background
Tone: Informative but not alarmist

Structure:
1. Introduction: Why AI safety matters (100 words)
2. Challenge 1: Alignment problem (125 words)
3. Challenge 2: Unintended consequences (125 words)
4. Challenge 3: Transparency and accountability (125 words)
5. Conclusion: Path forward (25 words)

Requirements:
- Use analogies for complex concepts
- Cite specific examples
- 8th-grade reading level
- Avoid technical jargon
```

### Version 4 (Adding Examples & Verification)
```
[Previous version]

Examples of good analogies:
- AI alignment: Like programming a robot to "make humans happy"
  but it might do so by forcibly administering drugs
- Unintended consequences: Like the sorcerer's apprentice

After writing:
1. Verify reading level using Hemingway Editor standards
2. Check that each section meets word count
3. Confirm no technical terms without explanation
```

---

## Next Steps

### Now You Know:
- ✓ How to structure clear prompts
- ✓ Essential components (role, task, format)
- ✓ Common mistakes to avoid
- ✓ How to iterate and improve

### Next Level:
1. **Read:** [Prompt Engineering Best Practices](./Prompt-Engineering-Best-Practices-2025.md)
2. **Learn:** [Advanced Techniques](./Advanced-Prompting-Techniques-2025.md)
3. **Understand:** [Context Engineering](./Context-Engineering-Guide-2025.md)
4. **Practice:** Use the [code examples](../examples/)

### Practice Exercise

Try improving this prompt:

**Original:**
```
Help me plan a vacation.
```

**Your improved version:**
```
[Your answer here - aim for 5-10 lines with role, context, task, format]
```

**Sample answer:**
```
You are a travel advisor specializing in European destinations.

I want to plan a 7-day vacation to Italy in September for 2 adults.
Budget: $5000 total. Interests: history, food, and photography.

Provide:
1. Recommended cities (2-3 cities with time allocation)
2. Daily itinerary (key activities and meals)
3. Budget breakdown (flights, hotels, food, activities)
4. Packing tips (weather-appropriate)
5. Photography recommendations (best locations and times)

Format as a detailed day-by-day plan with costs.
```

---

## Quick Reference Card

**BASIC FORMULA:**
```
ROLE + TASK + FORMAT + CONSTRAINTS = Good Prompt
```

**STARTER TEMPLATE:**
```
You are [role].

[Task description]

Provide:
1. [Output requirement 1]
2. [Output requirement 2]
3. [Output requirement 3]

Format: [structure specification]
Constraints: [limits and requirements]
```

**REMEMBER:**
- Be specific
- Provide context
- Show examples
- Specify format
- Test and iterate

---

## Resources

### Documentation
- [Complete Best Practices Guide](./Prompt-Engineering-Best-Practices-2025.md)
- [Context Engineering](./Context-Engineering-Guide-2025.md)
- [Advanced Techniques](./Advanced-Prompting-Techniques-2025.md)
- [Prompt Frameworks Guide](../Prompt-Frameworks-Guide.md)

### Code Examples
- [Python Examples](../examples/prompt_engineering_examples.py)
- [Example README](../examples/README.md)

### External Resources
- [OpenAI Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Claude Prompting](https://docs.anthropic.com/en/docs/prompt-engineering)
- [Prompting Guide](https://www.promptingguide.ai/)

---

**Congratulations!** 🎉

You now know the fundamentals of prompt engineering. The key is practice:
- Start with simple prompts
- Iterate based on results
- Learn from what works
- Build your own prompt library

*Last updated: January 2025*
