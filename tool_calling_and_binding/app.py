import os
from dotenv import load_dotenv
load_dotenv()

from groq import Groq
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import create_react_agent, AgentExecutor
from langsmith import Client
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import load_tools
from langchain_classic.chains.llm_math.prompt import PROMPT
from langchain_core.tools import tool
import numexpr
import wikipedia.wikipedia as wp_mod

wp_mod.USER_AGENT = "Assignment32Bot/1.0 (vichi.techsaga@gmail.com)"






## Task 2:  Built-in Tools in LangChain




