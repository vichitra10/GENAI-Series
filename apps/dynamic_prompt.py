# Prompt Template or Dynamic Template
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()

from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)

llm = ChatOpenAI(model = "gpt-4o")

# Static Prompts
prompts = [
    { "role":"system", "content": " You are a python developer"},
    {"role":"user", "content":"what is python"}
]
response = llm.invoke(prompts)
# print(response.content)

# Dynamic Prompts

prompts = [
    { "role":"system", "content": " You are a translator and translate input in {language} ?"},
    {"role":"user", "content":"{query}"}
]
final_prompts = prompts.format_message(language = "Hindi", query = "I love Python and JavaScript")
res = llm.invoke(final_prompts)
print(res.content)
