from dotenv import load_dotenv
# from langchain_groq import ChatGroq
from groq import Groq
load_dotenv()

## Task 1 Groq Api Setup and Basic Chat
print("Groq SDK installed successfully!")
# model = ChatGroq(model="openai/gpt-oss-120b",temperature=0)
# response = model.invoke('How LLM Works. Explain only 100 words')
# print(response.content)

client = Groq()

response  = client.chat.completions.create(model = "openai/gpt-oss-120b",temperature=0,messages= [{"role": "user", "content":"What is Groq in 250 words"  }] )

# print(response.choices[0].message.content)  


## Task 2: Build a groq ChatBot (Core Logic)

def groq_chat(prompt: str):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Give clear and simple answers only in 250 words."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

answer = groq_chat('How GENAI Works')
# print(answer)


## Here we are trying to check with multiple prompts
prompts = [
    "What is Python?",
    "What is an LLM?",
    "Explain LangChain in simple words.",
    "What is the difference between AI and Generative AI?"]

for prompt in prompts:
     print("Question:", prompt)
     print("Answer:", groq_chat(prompt))
     print("-" * 50)
    
