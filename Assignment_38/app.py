import os
import re
import streamlit as st
import numexpr
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
# from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from code_assistant import generate_code


import ollama


response = ollama.chat(
    model="codellama:7b",
    messages=[
        {
            "role": "user",
            "content": "Write a Python function to check prime numbers."
        }
    ]
)

# print(response["message"]["content"])

## Task 3: Code Assistant Feature
llm = ChatOllama(
    model="codellama:7b",
    temperature=0
)
response = llm.invoke(
    "Write a Python function to check whether a number is prime."
)

# print(response.content)

result = generate_code(
    requirement="Create a function to find duplicate elements in a list.",
    language="Python"
)

print(result)