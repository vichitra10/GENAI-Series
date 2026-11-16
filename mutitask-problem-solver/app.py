import os
import re
import streamlit as st
import numexpr
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

try:
    from langchain.agents import create_tool_calling_agent, AgentExecutor
except ImportError:
    from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

st.title("Text to Math Problem Solver Using Groq OpenAI")

default_groq_api = os.getenv("GROQ_API_KEY")

groq_api = st.sidebar.text_input("Groq API Key (optional)", type="password")
api_key = groq_api.strip() if groq_api.strip() else default_groq_api

if not api_key:
    st.info("Please provide your Groq API Key (sidebar or .env file)")
    st.stop()

# ---------------- Model ----------------
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    groq_api_key=api_key,
)

# ---------------- Tools ----------------
wikipedia_wrapper = WikipediaAPIWrapper()

@tool
def wikipedia(query: str) -> str:
    """Look up facts about people, places, companies and concepts on Wikipedia."""
    return wikipedia_wrapper.run(query)

@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression such as '(25*4)+10/2'. Input must be only the expression."""
    expr = "".join(re.findall(r"[\d\.\+\-\*\/\^\(\)%\s]+", expression)).strip().replace("^", "**")
    try:
        return str(numexpr.evaluate(expr))
    except Exception as e:
        return f"Could not evaluate '{expr}': {e}"

reasoning_prompt = ChatPromptTemplate.from_messages([
    ("system", "Do not call any tools or functions. Solve the problem logically and "
               "display the solution point-wise in plain text."),
    ("human", "{question}"),
])
reasoning_chain = reasoning_prompt | model | StrOutputParser()

@tool
def reasoning(question: str) -> str:
    """Answer logic puzzles, word problems and multi-step reasoning questions. Input is the full question."""
    last_error = None
    for _ in range(3):
        try:
            return reasoning_chain.invoke({"question": question})
        except Exception as e:
            last_error = e
            if "tool_use_failed" not in str(e):
                raise
    return f"Reasoning failed after 3 attempts: {last_error}"

tools = [wikipedia, calculator, reasoning]

# ---------------- Agent (with chat history) ----------------
agent_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a math and reasoning assistant. Use the calculator tool for arithmetic, "
     "the reasoning tool for logic and word problems, and wikipedia for factual lookups. "
     "For simple general questions, answer directly. Present the final answer point-wise."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(model, tools, agent_prompt)
assistant_agent = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, max_iterations=5)

# ---------------- UI ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I am a Math Chatbot who can answer your questions."}
    ]

def build_history():
    history = []
    for m in st.session_state.messages[1:]:  # skip the greeting
        if m["role"] == "user":
            history.append(HumanMessage(content=m["content"]))
        else:
            history.append(AIMessage(content=m["content"]))
    return history

# 1) Show stored history first
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 2) Chat input stays pinned at the bottom
question = st.chat_input("Please ask your question")

if question and question.strip():
    history = build_history()  # take history BEFORE adding the new question

    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        with st.spinner("Generating Response..."):
            try:
                if re.fullmatch(r"[\d\s()+\-*/.^%]+", question.strip()):
                    response = calculator.invoke({"expression": question})
                else:
                    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                    result = assistant_agent.invoke(
                        {"input": question, "chat_history": history},
                        {"callbacks": [st_cb]},
                    )
                    response = result["output"]
            except Exception as e:
                response = f"Sorry, something went wrong: {e}"
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})