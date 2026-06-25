from dotenv import load_dotenv
load_dotenv()

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver  

from langchain.agents import create_agent
from pprint import pprint

llm = ChatGroq(model = "openai/gpt-oss-20b")
search = GoogleSerperAPIWrapper()
memory = InMemorySaver()
# res = search.run("Address of Techsaga Corporation Pvt Ltd")
# print(res)

# Now we are creating an agent with the help of llm and tools 
agent = create_agent(
    model=llm,
    tools= [search.run],
    system_prompt="You are an agent and can search any question on google",
    checkpointer=memory
)

# question = "What is the address of Techsaga COrporation Private Limited"

while True:
    query = input("User Question: ")
    if query.lower() == "quit":
        print("Good bye")
        
    break
thread_config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": query}]},
    config=thread_config
)
# pprint(response["messages"])
print(response["messages"][-1].content)

