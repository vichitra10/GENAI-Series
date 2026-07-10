from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver


# -------------------------------
# LLM
# -------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b"
)


# -------------------------------
# Tool
# -------------------------------

search = GoogleSerperAPIWrapper()

tools = [search.run]


# -------------------------------
# Session State
# -------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "memory" not in st.session_state:
    st.session_state.memory = InMemorySaver()


# -------------------------------
# Agent
# -------------------------------

agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=st.session_state.memory,
    system_prompt=(
        "You are an amazing AI assistant. "
        "You can answer questions and use Google Search whenever required."
    ),
)


# -------------------------------
# Streamlit UI
# -------------------------------

st.set_page_config(
    page_title="QuickAnswer",
    page_icon="🤖"
)

st.title("🤖 QuickAnswer")

st.subheader("Answer at the speed of thought")


# -------------------------------
# Display Previous Chat
# -------------------------------

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -------------------------------
# Chat Input
# -------------------------------

query = st.chat_input("Ask me anything...")

if query:

    # Display User Message
    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.history.append(
        {
            "role": "user",
            "content": query,
        }
    )

    # Invoke Agent
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": "1"
            }
        }
    )

    answer = response["messages"][-1].content

    # Display Assistant Response
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.history.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )