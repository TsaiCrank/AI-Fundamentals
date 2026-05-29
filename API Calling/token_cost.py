#!/usr/bin/env python3
"""
Task 5: Understanding Tokens and Business Costs
Learn how tokens work and calculate real business costs for AI usage.
"""

import openai
import os

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")
)

# Make an API call with a business-relevant prompt
prompt = "Explain the benefits of using AI for customer support in a business"
response = client.chat.completions.create(
    model="openai/gpt-4.1-mini",
    messages=[{"role": "user", "content": prompt}]
)

# Extract the token counts from response.usage
input_tokens = response.usage.prompt_tokens   # TODO: prompt_tokens
output_tokens = response.usage.completion_tokens   # TODO: completion_tokens
total_tokens = response.usage.total_tokens

# GPT-4.1-mini pricing (per 1,000 tokens)
input_price_per_1k = 0.0008   # That's $0.80 per million tokens
output_price_per_1k = 0.0032  # That's $3.20 per million tokens

# Calculate actual costs for this API call
input_cost = (input_tokens / 1000) * input_price_per_1k
output_cost = (output_tokens / 1000) * output_price_per_1k
total_cost = input_cost + output_cost
