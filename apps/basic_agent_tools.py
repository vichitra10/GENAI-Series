from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent

llm  = ChatOpenAI(model = "gpt-4o-mini")

@tool
def  addNumber(a:int, b:int):
    """It will return the sum of two numbers

    Args:
        a (int): _description_
        b (int): _description_
    """
    return a + b
# invoke the functions
# result = addNumber.invoke({"a":12, "b":50})
# print(result)


agent = create_agent(
    model = llm,
    tools = [addNumber],
    system_prompt="You are a math teacher and always use tool for calculation"
)

response = agent.invoke({'messages': [{"role":"user", "content": "What is 3+ 5 ?"}]})
print(response["messages"][-1].content)
