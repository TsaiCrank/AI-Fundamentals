import os
from langchain_openai import ChatOpenAI

# Initialize OpenAI model
openai_llm = ChatOpenAI(
        model="openai/gpt-4.1-mini",
        api_key=os.getenv("OPENAPI_API_KEY"),
        base_url=os.getenv("OPENAPI_API_BASE")
    )

# Initialize Google Gemini model
print("Setting up Google Gemini...")
google_llm = ChatOpenAI(
        model="google/gemini-2.5-flash",
        api_key=os.getenv("OPENAPI_API_KEY"),
        base_url=os.getenv("OPENAPI_API_BASE")
    )

# Initialize X.AI Grok model
print("Setting up X.AI Grok...")
xai_llm = ChatOpenAI(
        model="x-ai/grok-4.3",
        api_key=os.getenv("OPENAPI_API_KEY"),
        base_url=os.getenv("OPENAPI_API_BASE")
    )

test_prompt = "Explain cloud computing in one sentence"

# Test all models with the same prompt
if openai_llm:
        response = openai_llm.invoke(test_prompt)
        print(f"OpenAI: {response.content[:100]}...")

if google_llm:
        response = google_llm.invoke(test_prompt)
        print(f"Google: {response.content[:100]}...")

if xai_llm:
        response = xai_llm.invoke(test_prompt)
        print(f"X.AI: {response.content[:100]}...")
