from langchain_groq import ChatGroq
from custom_toolkit import CompanyToolkit

## Step 1 : Bind the tools to the LLM

llm = ChatGroq(
    model = "openai/gpt-oss-120b",
    temperature = 0
)

tools = CompanyToolkit().get_tools()

llm_with_tools = llm.bind_tools(tools)

print("Tools bound to the LLM:")
for t in tools:
    print(f"  - {t.name}")



# Step 2: Let the LLM decide when to call which tool
# (We only look at the LLM's decision here; we do NOT run the tools.)
# ---------------------------------------------------------------

queries = [
    "How many paid leaves do employees get per year?",   # -> policy_lookup
    "Who works in the Engineering department?",          # -> database_query
    "What is today's date?",                             # -> datetime_tool
    "Hello! How are you today?",                         # -> no tool needed
    "What is the capital of France?",                    # -> no tool needed
]

for q in queries:
    print(f"\n==== Query: {q}")
    ai_msg = llm_with_tools.invoke(q)
 
    if ai_msg.tool_calls:
        for call in ai_msg.tool_calls:
            print(f"  LLM decided to call: {call['name']}")
            print(f"  With arguments     : {call['args']}")
    else:
        print("  LLM decided NO tool is needed.")
        print(f"  Direct answer: {ai_msg.content}")

