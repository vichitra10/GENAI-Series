## Build Stateful Chatbot Application


import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, trim_messages

load_dotenv()

# 1. Configure the page
st.set_page_config(page_title="Stateful Chatbot", page_icon="💬")

st.title("💬 Stateful Chatbot")
st.caption("A chatbot with conversation history and message trimming")

# 2. Initialize the LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

# 3. Create the prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a helpful Q&A chatbot.

        Rules:
        - Answer in a maximum of 100 words.
        - Prefer short paragraphs or bullet points.
        - Do not give long explanations unless explicitly requested.
        - Use conversation history to understand follow-up questions.
        """
    ),
    MessagesPlaceholder(variable_name="history")
])

# 4. Create the chain
chain = prompt | llm


# 5. Function to trim chat history
def trim_history(history):
    return trim_messages(
        history,
        max_tokens=50,
        token_counter="approximate",
        strategy="last",
        allow_partial=False,
        start_on="human"
    )


# 6. Initialize conversation history
if "history" not in st.session_state:
    st.session_state.history = []


# 7. Display previous messages
for message in st.session_state.history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)

    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)


# 8. Accept a new question
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Display the current question
    with st.chat_message("user"):
        st.write(user_input)

    # Trim old history before adding the new question
    st.session_state.history = trim_history(
        st.session_state.history
    )

    # Store the current user message
    st.session_state.history.append(
        HumanMessage(content=user_input)
    )

    # Generate the answer using conversation history
    try:
        response = chain.invoke({
            "history": st.session_state.history
        })

        # Display the answer
        with st.chat_message("assistant"):
            st.write(response.content)

        # Save the AI response
        st.session_state.history.append(
            AIMessage(content=response.content)
        )

        # Trim the saved history
        st.session_state.history = trim_history(
            st.session_state.history
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")


# 9. Clear conversation
if st.button("Clear Chat"):
    st.session_state.history = []
    st.rerun()


## Task 7: Observation and Insights (short question answer)
## Q.1: Why chat history is important
## Ans: Chat history is important because it allows a chatbot to remember previous messages and understand the context of conversation instead of treating every question as a new conversation.

## Q.2: Trade-off between long memory and performance
## Ans: The trade-off between long memory and performance means balancing how much conversation history a chatbot remembers against how quickly and efficient it responds.

## Q.3: When to summarize and trim history
## Ans: Trim history when the conversation gets long and you only need recent messagea. It reduce token usage , cost , and response time.
## Summarize History when older information is still important. It preserves key details in a shorter form.

## Q.4: Difference between messageplaceholder and memory?
## Ans: Memory stores  and manage previous conversation messages so the chatbot can remember them.
## MessagePlaceHolder : Speciifies where those previous messages are inserted into the prompt for the AI to use.
