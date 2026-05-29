import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import CommaSeparatedListOutputParser

def main():
    print("🎯 Task 5: Chain Composition with |")
    print("=" * 50)

    # Initialize LLM once
    llm = ChatOpenAI(
        model="openai/gpt-4.1-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
        temperature=0.3
    )

    # Chain 1: Simple Analysis Chain
    print("\n⛓️ Chain 1: Simple Analysis")
    print("=" * 50)

    # Create analysis prompt
    analysis_prompt = PromptTemplate(
        template="Analyze {technology} and provide pros and cons in 2-3 sentences",
        input_variables=["technology"]
    )

    # String parser for text output
    str_parser = StrOutputParser()

    # Build analysis chain using pipe operator
    analysis_chain = analysis_prompt | llm | str_parser

    # Test the analysis chain
    if analysis_chain:
        result = analysis_chain.invoke({
            "technology": "blockchain"
        })
        print(f"📝 Input: 'Analyze blockchain'")
        print(f"✅ Output: {result}")

    # Chain 2: List Generation Chain
    print("\n⛓️ Chain 2: List Generation with Parser")
    print("=" * 50)

    # Create list prompt
    list_prompt = PromptTemplate(
        template="List 3 use cases for {technology} (comma-separated):",
        input_variables=["technology"]
    )

    # List parser for structured output
    list_parser = CommaSeparatedListOutputParser()

    # Build list chain with different parser
    list_chain = list_prompt | llm | list_parser  # Replace ___ with: list_prompt, llm, list_parser

    # Test the list chain
    if list_chain:
        result = list_chain.invoke({
            "technology": "blockchain"
        })
        print(f"📝 Input: 'List use cases for blockchain'")
        print(f"✅ Output: {result}")
        print(f"✅ Type: {type(result)} - Python list!")

    # Demonstrate the power of chains
    print("\n🎉 Complete Pipeline Example")
    print("=" * 50)

    test_tech = "artificial intelligence"
    print(f"Technology: {test_tech}\n")

    # Run both chains on the same input
    if analysis_chain and list_chain:
        # Chain 1: Get analysis
        analysis = analysis_chain.invoke({"technology": test_tech})
        print(f"1️⃣ Analysis:\n   {analysis}")

        # Chain 2: Get use cases
        use_cases = list_chain.invoke({"technology": test_tech})
        print(f"\n2️⃣ Use Cases:")
        for i, use_case in enumerate(use_cases, 1):
            print(f"   {i}. {use_case}")

if __name__ == "__main__":
    main()