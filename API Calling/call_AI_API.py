#Import OpenAI libraries
import openai
import os

# Initialize the OpenAI client
client = openai.OpenAI(
    api_key=os.getenv("OPEN_API_KEY"),
    base_url=os.getenv("OPEN_API_BASE")
)

response = client.chat.completions.create(
     model="openai/gpt-4.1-mini",  # which AI model to use
     messages=[
         {
             "role": "user",     # Use "user" - you're the user speaking
             "content": "Hello AI, please introduce yourself"   #your message
         }
     ]
 )

"""
ChatCompletion(
    id='gen-1758773976-Ek9OxTgdgkP4Mo3ub6qf',
    choices=[
        Choice(
            finish_reason='stop',
            index=0,
            message=ChatCompletionMessage(
                content="Hello! I'm ChatGPT, an AI language model created by OpenAI. I'm here to help with a wide range of tasks such as answering questions, providing explanations, generating creative content, assisting with writing, and much more. How can I assist you today?",
                role='assistant'
            )
        )
    ],
    created=1758773976,
    model='openai/gpt-4.1-mini',
    object='chat.completion',
    usage=CompletionUsage(
        completion_tokens=55,
        prompt_tokens=13,
        total_tokens=68
    )
)
"""
# Extract the AI's text response using the exact path
ai_text = response.choices[0].message.content