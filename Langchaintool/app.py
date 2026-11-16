from langchain_groq import ChatGroq
from langchain_core.tools import tool
import requests
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv

from langchain_classic.agents import  create_react_agent , AgentExecutor
from langchain_classic import hub
from langsmith import Client

import inspect


load_dotenv()

print(inspect.signature(hub.pull))
print("Pull:", inspect.signature(hub.pull))
print("Push:", inspect.signature(hub.push))


# from langchain_core.prompts import PromptTemplate

# prompt = hub.pull("my-first-prompt:72656cb6")
prompt = hub.pull("hwchase17/react")

print(prompt)




# # Create a prompt
# prompt = PromptTemplate.from_template(
#     "Answer this question: {question}"
# )

# # Push prompt to LangSmith Hub
# result = hub.push(
#     "your-username/my-first-prompt",
#     prompt
# )

# print("Prompt pushed:", result)

# # Pull prompt from LangSmith Hub
# pulled_prompt = hub.pull(
#     "your-username/my-first-prompt"
# )

# print("Prompt pulled:", pulled_prompt)

# llm = ChatGroq(
#       model="openai/gpt-oss-120b",
#       temperature=0)

# # print('tool file working')
# prompt = hub.pull('hwchase17/react',
#                    dangerously_pull_public_prompt=True)
# print(prompt)

# client = Client()

# prompt = client.pull_prompt(
#     "hwchase17/react",
#     dangerously_pull_public_prompt=True
# )

# print(prompt)

