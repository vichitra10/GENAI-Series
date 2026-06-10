from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash"
)

# Page Title
st.title("🤖 Ask Buddy - AI QnA Bot")
st.markdown("My QnA Bot with LangChain and Google Gemini!")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
query = st.chat_input("Ask Anything...")

if query:

    # Show User Message
    st.session_state.messages.append(
        {"role": "user", "content": query}
    )

    with st.chat_message("user"):
        st.markdown(query)

    # Get AI Response
    response = llm.invoke(query)

    # Store AI Response
    st.session_state.messages.append(
        {"role": "assistant", "content": response.content}
    )

    # Show AI Response
    with st.chat_message("assistant"):
        st.markdown(response.content)