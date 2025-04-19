# Prompt Engineering Guide for Sample Datasets

This guide provides practical examples of how to craft effective prompts for analyzing and working with the provided datasets. Each section includes sample prompts and explanations of the techniques used.

## General Prompt Engineering Principles

1. **Be Specific and Clear**
   - ❌ "Analyze this data"
   - ✅ "Analyze the customer feedback data to identify the top 3 most common complaints about AI tools"

2. **Use Step-by-Step Instructions**
   - ❌ "Summarize everything"
   - ✅ "First, identify the key themes in the news articles. Then, create a 3-sentence summary for each article, focusing on the main discovery and its implications."

3. **Provide Context and Format**
   - ❌ "Give me the data in JSON"
   - ✅ "Transform the customer feedback into a JSON structure where reviews are grouped by product, including rating averages and common themes in the feedback"

## Dataset-Specific Prompt Examples

### 1. Customer Feedback Analysis (customer_feedback.csv)

```markdown
# Basic Analysis Prompt
"Analyze the customer feedback for AI services and provide:
1. The average rating for each product
2. Common positive themes across all 5-star reviews
3. Recurring improvement suggestions from reviews rated 3 stars or lower"

# Sentiment Analysis Prompt
"For each AI service in the dataset:
1. Identify the emotional tone of the feedback (positive, negative, neutral)
2. Extract specific feature requests or improvement suggestions
3. Categorize the feedback into: UI/UX, Performance, Reliability, and Features"

# Comparative Analysis Prompt
"Compare ChatGPT Plus and Claude based on the feedback:
1. List their respective strengths
2. Identify their main differences
3. Suggest potential improvements for each"
```

### 2. News Article Processing (news_articles.txt)

```markdown
# Summarization Prompt
"For each news article:
1. Create a one-sentence TLDR
2. Extract the key scientific or technological advancement
3. List potential future implications
Format the output as a bulleted list."

# Pattern Analysis Prompt
"Analyze these articles to:
1. Identify common themes across all articles
2. Extract all quoted expert opinions
3. Create a timeline of developments
4. Suggest potential follow-up questions for each story"
```

### 3. Product Catalog Analysis (products.json)

```markdown
# Feature Analysis Prompt
"Using the products.json data:
1. Compare the feature sets of all products
2. Identify patterns in user satisfaction relative to price
3. Generate a summary of the most valued features based on positive reviews
Format the response as a structured report."

# Review Analysis Prompt
"For each product in the catalog:
1. Extract key phrases from positive and negative reviews
2. Identify specific user pain points
3. Suggest potential product improvements based on the feedback
Present findings in a table format."
```

### 4. Airline Safety Data (airline-safety.csv)

```markdown
# Statistical Analysis Prompt
"Analyze the airline safety data to:
1. Identify trends in safety incidents over time
2. Compare safety records across different airlines
3. Calculate the correlation between airline size and safety record
Present findings with specific numbers and percentages."

# Report Generation Prompt
"Create a comprehensive safety report that:
1. Identifies the safest airlines based on the data
2. Highlights significant safety improvements over time
3. Provides context for interpreting the statistics
Format as an executive summary with key findings."
```

## Advanced Techniques

### 1. Chain-of-Thought Prompting
```markdown
"Let's analyze the customer feedback step by step:
1. First, list all unique AI services mentioned
2. For each service, calculate:
   - Average rating
   - Number of reviews
   - Most frequent positive words
   - Most frequent negative words
3. Then, synthesize this information to:
   - Identify market leaders
   - Spot common pain points
   - Suggest industry-wide improvements"
```

### 2. Role-Based Prompting
```markdown
"As a Product Manager analyzing the AI services feedback:
1. What are the top 3 feature requests?
2. Which competitors are mentioned positively?
3. What price points are considered acceptable?
4. What quick wins could improve user satisfaction?"
```

### 3. Format-Driven Prompting
```markdown
"Transform the news articles into a structured format:
{
  'title': '',
  'date': '',
  'key_discovery': '',
  'expert_opinion': '',
  'implications': [],
  'industry_impact': ''
}
Include all three articles in this format."
```

## Tips for Getting Better Results

1. **Iterate and Refine**
   - Start with a basic prompt
   - Analyze the response
   - Add constraints or specifications
   - Refine until you get desired output

2. **Use System Context**
   - Set the role/expertise level needed
   - Specify output format upfront
   - Include error handling preferences

3. **Combine Techniques**
   - Mix statistical analysis with narrative insights
   - Combine multiple data sources for richer analysis
   - Use both quantitative and qualitative approaches

Remember: The best prompts are clear, specific, and structured to guide the AI toward producing exactly the type of analysis or output you need. 