# 🚀 Prompt Engineering Mastery: Exercises from Google's Playbook

*Based on Google's Prompt Engineering Whitepaper (2024)*

[Reference: Google Prompt Engineering Whitepaper](https://www.kaggle.com/whitepaper-prompt-engineering)

## 📚 Introduction

This document contains practical exercises to help you master prompt engineering techniques based on Google's comprehensive playbook. These exercises are designed to help you understand how to craft effective prompts for large language models (LLMs) like Gemini, improving the quality, relevance, and usefulness of AI-generated outputs.

## 🎯 Exercise 1: Clear and Specific Instructions

**Concept:** Providing clear, specific, and well-structured instructions helps the model generate more accurate and useful responses.

**Exercise:**
1. Write a prompt asking an LLM to explain quantum computing to a 10-year-old, specifying the length (3-4 paragraphs) and tone (friendly and simple)
2. Create a prompt to generate a list of ideas for reducing plastic waste, specifying that each idea should include both the action and its environmental impact
3. Write a prompt to summarize a scientific article, specifying the format (bullet points) and key aspects to include (methodology, findings, implications)

**Challenge:** Compare responses from prompts with vague instructions versus detailed instructions. How does specificity improve the quality of responses?

## 🔄 Exercise 2: Few-Shot Learning

**Concept:** Few-shot prompting involves providing one or more examples of the desired input-output pairs to guide the model's response.

**Exercise:**
1. Create a one-shot prompt to classify movie reviews as positive or negative
   ```
   Task: Classify the sentiment of movie reviews
   
   Example:
   Input: "The movie was fantastic!"
   Output: Positive
   
   Input: "I was disappointed by the plot."
   Output: 
   ```

2. Create a few-shot prompt (3 examples) to generate creative product names for eco-friendly water bottles, using a consistent format for each example
   ```
   Task: Generate creative product names for eco-friendly water bottles
   
   Example 1:
   Features: Made from bamboo, keeps drinks cold for 24 hours
   Name: FrostGrove
   
   Example 2:
   [Your example here]
   
   Example 3:
   [Your example here]
   
   Features: Made from recycled ocean plastic, colorful design
   Name:
   ```

3. Compare zero-shot, one-shot, and three-shot prompts for translating technical jargon into simple language

**Challenge:** Experiment with varying numbers of examples (1, 3, 5) for the same task. What is the optimal number for producing the best results?

## 🧠 Exercise 3: Chain of Thought (CoT) Prompting

**Concept:** Chain of Thought encourages the model to break down complex reasoning into intermediate steps, improving accuracy for tasks that require reasoning.

**Exercise:**
1. Write a CoT prompt for solving a math word problem, using phrases like "Let's think through this step-by-step" or "Let's solve this systematically"
   ```
   Solve this problem step-by-step:
   
   A store is having a 25% off sale. If a shirt originally costs $40, how much would you save, and what is the final price?
   
   Step 1:
   ```

2. Create a CoT prompt for analyzing the ethical implications of a new technology, breaking the analysis into distinct components (benefits, risks, stakeholders)

3. Develop a CoT prompt for troubleshooting a computer issue, where you explicitly ask the model to (1) identify possible causes, (2) suggest diagnostics, and (3) recommend solutions

**Challenge:** Compare responses from standard prompts versus CoT prompts for the same complex questions. How does the reasoning quality differ?

## 🎭 Exercise 4: Role Prompting

**Concept:** Role prompting involves asking the LLM to assume a specific role or persona, which can improve responses for specialized knowledge or perspectives.

**Exercise:**
1. Write a prompt where the LLM takes on the role of a cybersecurity expert explaining password best practices to a non-technical audience
   ```
   You are a cybersecurity expert speaking to a group of non-technical business professionals. 
   Explain password best practices in simple terms, avoiding jargon where possible. Include:
   1. What makes a strong password
   2. Common mistakes to avoid
   3. Practical tips for password management
   ```

2. Create a prompt where the LLM acts as a historical figure (e.g., Leonardo da Vinci) describing modern technology (e.g., smartphones)

3. Develop a prompt where the LLM plays the role of a career counselor providing advice to someone transitioning careers into technology

**Challenge:** Try the same question with three different roles (e.g., expert, teacher, friend). How does the content, tone, and advice change?

## 📝 Exercise 5: Format Control

**Concept:** Controlling the format of the AI-generated output by explicitly requesting specific structures improves the usability of responses.

**Exercise:**
1. Write a prompt to generate information about renewable energy sources in a markdown table format with specified columns (Type, Pros, Cons, Global Adoption)
   ```
   Generate a comparison of three renewable energy sources in a markdown table format with these columns:
   | Energy Source | How It Works | Main Advantages | Main Challenges | Global Adoption |
   ```

2. Create a prompt to get a recipe for sourdough bread with numbered steps, ingredient quantities in both metric and imperial units, and preparation time clearly indicated

3. Develop a prompt requesting information about different programming languages in JSON format with specific fields (name, primaryUses, learningCurve, averageSalary, popularFrameworks)

**Challenge:** Request the same information in three different formats (e.g., paragraph, table, list). Which format is most effective for your specific use case?

## 🔍 Exercise 6: Contextual Prompting

**Concept:** Providing relevant context in your prompt helps the model generate more accurate and tailored responses.

**Exercise:**
1. Write a prompt asking for an explanation of climate change that includes contextual information about the audience (e.g., "for elementary school students")

2. Create a prompt for a tweet-length summary of a historical event, providing key dates and figures as context

3. Develop a prompt that includes both brief context (2-3 sentences) and comprehensive context (paragraph) about vaccines, and compare the responses

**Challenge:** Experiment with different amounts of context. How does adding specific contextual details improve the relevance and accuracy of responses?

## 🧩 Exercise 7: Prefixes and Completion Patterns

**Concept:** Using prefixes for different parts of the prompt and letting the model complete partial patterns can guide responses effectively.

**Exercise:**
1. Design a prompt using prefixes for different parts ("Context:", "Question:", "Format:", "Example:") to classify emails into categories
   ```
   Context: You're helping organize emails into categories.
   Categories: Personal, Work, Marketing, Spam
   
   Example 1:
   Email: "Hi John, can we meet for coffee this Saturday?"
   Category: Personal
   
   Example 2:
   Email: "FINAL NOTICE: Your account will be suspended"
   Category: Spam
   
   Email: "Meeting notes from yesterday's product review"
   Category:
   ```

2. Create a prompt where you start an outline format and let the model complete it
   ```
   Create an outline for a research paper on artificial intelligence ethics.
   
   I. Introduction
     A. Definition of AI ethics
     B. 
   ```

3. Develop a prompt system using prefixes to separate user input from response templates

**Challenge:** Create a partial JSON structure and let the model complete it based on given information. Compare this with asking for JSON format in the instructions.

## 🎨 Exercise 8: Parameter Experimentation

**Concept:** Adjusting model parameters like temperature, top-K, and top-P can significantly affect the creativity, diversity, and determinism of responses.

**Exercise:**
1. Write a prompt to generate creative story ideas, then test it with three different temperature settings (0.2, 0.7, 1.0) and compare results

2. Create a prompt for generating a factual paragraph about space exploration, testing different combinations of top-K and top-P values

3. Develop a prompt that generates multiple solutions to a business problem, experimenting with temperature settings to find the optimal balance between creativity and practicality

**Challenge:** For a single well-crafted prompt, generate 5 responses at each of these temperatures: 0, 0.3, 0.7, 1.0. Analyze how temperature affects variance, creativity, and accuracy.

## 🧪 Exercise 9: Iterative Prompt Refinement

**Concept:** Prompt engineering is an iterative process that requires experimentation, evaluation, and refinement.

**Exercise:**
1. Start with a basic prompt to generate social media content, then iteratively refine it through at least 3 versions, documenting improvements
   ```
   Version 1: "Write a social media post about a new coffee shop."
   
   Version 2: "Write an Instagram post for a new artisanal coffee shop that specializes in single-origin beans."
   
   Version 3: [Your refined version]
   ```

2. Take a prompt that produces mediocre results and improve it using three different strategies:
   - Adding more specific instructions
   - Including examples
   - Restructuring the prompt format

3. Switch between different prompt approaches (zero-shot, few-shot, CoT) for a challenging task until you find the optimal approach

**Challenge:** Take a "failed" prompt that doesn't generate the desired output and transform it through at least 5 iterations until it produces excellent results. Document your thought process and what you learned.

## 🚀 Exercise 10: Complex Problem Decomposition

**Concept:** Breaking down complex prompts into simpler components improves model performance on sophisticated tasks.

**Exercise:**
1. Decompose the task of creating a comprehensive marketing plan into a series of smaller prompts, each addressing one component (target audience analysis, competitive research, messaging strategy, etc.)

2. Design a prompt chain where the output of one prompt becomes the input for the next prompt in a sequential process (e.g., brainstorming → selecting best ideas → developing detailed implementation plans)

3. Create a system for aggregating results from multiple specialized prompts into a cohesive final output

**Challenge:** Identify a complex task in your field and break it down into at least 5 separate prompts that work together to produce a sophisticated output. Test both the individual components and the complete system.

## 📊 Exercise 11: Output Evaluation and Optimization

**Concept:** Systematically evaluating and optimizing model outputs improves reliability and quality.

**Exercise:**
1. Create a prompt that includes evaluation criteria for the model to use in assessing its own output
   ```
   Generate a persuasive email to potential clients about our new consulting service.
   After generating the email, evaluate it against these criteria:
   - Clarity of value proposition
   - Compelling call to action
   - Professional tone
   - Absence of jargon
   Rate each aspect from 1-5 and suggest improvements.
   ```

2. Design a prompt system that allows you to generate multiple variants of the same content, then select and refine the best option

3. Develop a prompt that requests both a high-level summary and detailed content, allowing for multi-layered evaluation

**Challenge:** Create a standardized evaluation framework for assessing prompt effectiveness across 5 dimensions (accuracy, relevance, completeness, format adherence, and creativity). Apply it to outputs from various exercises.

## 🏆 Advanced Challenge: Comprehensive Prompt Engineering Project

Apply all the techniques you've learned to create a sophisticated prompt system for a real-world use case:

1. Choose a domain (e.g., healthcare, education, customer service)
2. Define a complex task that requires multiple types of prompts (e.g., content creation, data analysis, decision support)
3. Design a series of prompts that work together to accomplish the task, incorporating multiple techniques from this guide
4. Test and refine your prompts based on the responses, documenting your process
5. Create a final prompt template with clear instructions for others to use or adapt

## 🔑 Key Takeaways

- **Be specific and clear** in your instructions rather than vague
- **Include examples** whenever possible to guide model response format and quality
- **Use Chain of Thought** for complex reasoning tasks
- **Format matters** - structure your prompts consistently and request specific output formats
- **Context is crucial** - provide relevant background information
- **Iterate and experiment** with different prompt variations and parameter settings
- **Break down complex tasks** into simpler components
- **Evaluate systematically** against clear criteria
- **Consider model limitations** - especially for factual information and complex reasoning
- **Stay updated** on model capabilities and features

Happy prompting! 🎉 
