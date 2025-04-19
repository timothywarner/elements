# Custom AI Teaching Assistant Example

Welcome to the O'Reilly Live Learning Custom Assistant Example! This repository contains everything you need to build a specialized AI teaching assistant focused on prompt engineering and AI development concepts.

## Assistant Overview

This example demonstrates how to create a custom GPT assistant that helps students learn prompt engineering and AI development. The assistant is designed to:

1. **Teach Prompt Engineering Concepts**
   - Explain different prompting techniques
   - Provide real-world examples
   - Offer interactive exercises
   - Give feedback on student attempts

2. **Provide Technical Guidance**
   - Help with API integration
   - Explain best practices
   - Debug common issues
   - Share code examples

3. **Assess Learning**
   - Quiz students on concepts
   - Review prompt attempts
   - Provide constructive feedback
   - Track progress

## Directory Structure

```
knowledge-sources-for-assistant/
├── api-examples/
│   ├── openai_assistant.py
│   ├── custom_actions.py
│   └── requirements.txt
├── knowledge-base/
│   ├── prompt_engineering_patterns.json
│   ├── best_practices.md
│   └── common_mistakes.md
├── training-data/
│   ├── example_conversations.jsonl
│   ├── exercises.json
│   └── quiz_questions.json
└── functions/
    ├── code_analyzer.py
    ├── prompt_validator.py
    └── feedback_generator.py
```

## Getting Started

1. **Setup**
   ```bash
   pip install -r api-examples/requirements.txt
   ```

2. **Configuration**
   - Add your OpenAI API key to environment variables
   - Configure assistant parameters in `config.json`
   - Customize knowledge base as needed

3. **Running the Example**
   ```bash
   python api-examples/openai_assistant.py
   ```

## Knowledge Sources

This assistant is powered by various knowledge sources:

1. **Prompt Engineering Patterns**
   - Common patterns and their use cases
   - Best practices and guidelines
   - Anti-patterns to avoid

2. **Technical Documentation**
   - API integration guides
   - Code examples
   - Troubleshooting guides

3. **Interactive Exercises**
   - Practice problems
   - Real-world scenarios
   - Assessment questions

4. **Custom Functions**
   - Code analysis
   - Prompt validation
   - Feedback generation

## Custom Actions

The assistant includes several custom actions:

1. **analyzePrompt**
   - Evaluates prompt structure
   - Suggests improvements
   - Checks for best practices

2. **generateExample**
   - Creates relevant examples
   - Provides sample code
   - Shows expected outputs

3. **assessLearning**
   - Quizzes on concepts
   - Provides scoring
   - Offers improvement suggestions

## Use Cases

This assistant is particularly useful for:

1. **Educators**
   - Teaching prompt engineering concepts
   - Creating interactive exercises
   - Assessing student understanding

2. **Students**
   - Learning best practices
   - Getting immediate feedback
   - Practicing with real examples

3. **Developers**
   - Understanding API integration
   - Debugging issues
   - Implementing custom actions

## Best Practices

1. **Knowledge Base Management**
   - Keep information current
   - Structure data clearly
   - Include diverse examples

2. **Custom Action Design**
   - Make actions atomic
   - Include error handling
   - Provide clear feedback

3. **User Interaction**
   - Use clear prompts
   - Provide helpful feedback
   - Maintain conversation context

## Contributing

Feel free to contribute by:
1. Adding new knowledge sources
2. Improving existing content
3. Creating new exercises
4. Enhancing custom actions

## License

MIT License - Feel free to use and modify for your own teaching needs! 