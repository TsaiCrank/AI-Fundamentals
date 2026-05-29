import os

def raw_openai_approach():
    import openai

    # Create OpenAI client
    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE")
    )

    # Make API call (notice the complexity!)
    response = client.chat.completions.create(
        model="openai/gpt-4.1-mini",
        messages=[
            {"role": "user", "content": "Explain machine learning in one sentence"}
        ]
    )

    # Extract text (notice nested structure)
    if response:
        text = response.choices[0].message.content
        print(f"Response: {text[:100]}...")
        return text

    return None

def langchain_approach():
    from langchain_openai import ChatOpenAI

    # Initialize model (so simple!)
    llm = ChatOpenAI(
        model="openai/gpt-4.1-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE")
    )

    # Make the call (one line!)
    response = llm.invoke("Explain machine learning in one sentence")

    if response:
        print(f"Response: {response.content[:100]}...")
        return response.content

    return None

    # Run both approaches
    raw_result = raw_openai_approach()
    langchain_result = langchain_approach()
