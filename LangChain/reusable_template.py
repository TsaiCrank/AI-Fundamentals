import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

def main():
    print("🎯 Task 3: Dynamic Prompt Templates")
    print("=" * 50)

    print("\n📝 Creating a Reusable Template")
    print("=" * 50)

    # TODO 1: Create a versatile template
    template = PromptTemplate(
        input_variables=["topic", "style"],
        template="Explain {topic} in {style}"
    )

    # Test with actual LLM to show it works
    print("\n🤖 Testing Template with AI")
    print("=" * 50)

    # Initialize LLM
    llm = ChatOpenAI(
        model="openai/gpt-4.1-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
        temperature=0.7
    )

    # TODO 2: Use the template with LLM
    if template and llm:
        # Format the template with specific values
        test_prompt = template.format(
            topic="artificial intelligence",
            style="exactly 5 words"
        )

if __name__ == "__main__":
    main()