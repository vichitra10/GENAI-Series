from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import  InMemorySaver

# Gemini Model
llm = ChatGroq(model="openai/gpt-oss-20b", streaming=True)
search = GoogleSerperAPIWrapper()
tools = [search.run]
memory = InMemorySaver

if "memory" not in st.session_state:
 st.session_state.memory = InMemorySaver()

agent = create_agent(
    model = llm,
    tools = tools,
    checkpointer=st.session_state.memory,
    system_prompt= "You are an amazing ai agent and can search on google as well"
)



# Page Title
# st.subheader("🤖QuickAnswer - Answer at the speed  of thought")
st.markdown(
    "<h4 style='margin-bottom:0;'>🤖 QuickAnswer - Answer at the speed of thought</h4>",
    unsafe_allow_html=True
)
# Initialize Chat History

# Display Previous Messages
for message in st.session_state.history:
    role =  message["role"]
    content = message["content"]
    st.chat_message(message["role"]).markdown(message["content"])

# User Input
query = st.chat_input("Ask Anything...")

if query:

    # Show User Message
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role":"user","content":query},{"role":"user","content":query})

    # Get AI Response
    response = agent.stream(
        {"messages":[{"role":"user","content":query}]},
        {"configurable":{"thread_id":"1"}}
    )
    
    ai_container = st.chat_message("ai")
    with ai_container:
        space = st.empty()
        
        message = ''
        for chunk in response:
            message = message + chunk[0].content
            space.write(message)
        
    
    # answer = response["messages"][-1].content
    # st.chat_message
    
    

    # Store AI Response
    st.session_state.history.append(
        {"role": "assistant", "content": response.content}
    )

    # Show AI Response
    with st.chat_message("assistant"):
        st.markdown(response.content)