## Task 6: Tool Calling
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from custom_toolkit import CompanyToolkit

llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0, max_retries=5)

tools = CompanyToolkit().get_tools()
tool_map = {t.name: t for t in tools}
llm_with_tools = llm.bind_tools(tools)

def run_flow(query: str, max_rounds: int = 5) -> str:
    print("\n" + "=" * 70)
    print(f"[1] USER QUERY      : {query}")
    messages = [HumanMessage(query)]

    for round_no in range(1, max_rounds + 1):
        # [2] LLM reads the query (and any tool results so far)
        ai_msg = llm_with_tools.invoke(messages)

        print(ai_msg.content)
        

        # No tool requested -> this is the final answer
        if not ai_msg.tool_calls:
            print(f"[5] FINAL ANSWER    : {ai_msg.content}")
            return ai_msg.content    


         # [3] Tool selection (the LLM may pick one or several tools)
        print(f"[2] LLM (round {round_no})    : requested {len(ai_msg.tool_calls)} tool call(s)")
        for call in ai_msg.tool_calls:
            print(f"[3] TOOL SELECTED   : {call['name']}  args={call['args']}")

                 # [4] Tool execution
            result = tool_map[call["name"]].invoke(call["args"])
            print(f"[4] TOOL RESULT     : {result}")
 
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
 
    return "Stopped: too many tool rounds."    


if __name__ == "__main__":
    print("\n######## SINGLE TOOL QUERIES ########")
    single_tool_queries = [
        "How many days notice do I need to give before resigning?",   # policy_lookup
        "List the names of all employees in the HR department.",      # database_query
        "What is today's date and day of the week?",                  # datetime_tool
    ]
    for q in single_tool_queries:
        run_flow(q)
 
    print("\n\n######## MULTIPLE TOOL QUERIES ########")
    multi_tool_queries = [
        "What is Priya Verma's salary, and what is the work from home policy?",   # db + policy
        "What is today's date, who works in Finance, and what are the working hours?",  # all 3
    ]
    for q in multi_tool_queries:
        run_flow(q)



 ## Creating A ReAct AI Agent
 ## Task 7: ReAct Agent Overview

 ## Q.1: What is ReAct (Reason + Act)
 ## Ans: ReAct (Reason + Act) is a technique used in AI Agents where an LLM first reasons about a user's question, decides which action or tool is needed, executes that tool, and uses the result to generate an answer.

#  ReAct follows a cycle:
# 1. Reason: AI understands the user's question and decides what to do.
# 2. Act: AI selects and calls a tool.
# 3. Observe: AI receives the tool's result.
# 4. Repeat: AI may use another tool if needed.
# 5. Final Answer: AI generates the final response.

## Q.2: Why ReAct Agent are powerful ..?
## Ans: ReAct Agents are powerful because they can reason, use tools, observe results, and take multiple actions instead of only generating text like a normal LLM.
# 5 Reasons why ReAct Agents are powerful
# 1. Tool Usage: They can use tools such as databases, calculators, APIs, and search engines.
# 2. Real-time Information: They can retrieve updated information using external tools instead of relying only on training data.
# 3. Multi-step Problem Solving: They can break complex questions into smaller tasks and execute them step by step.
# 4. Decision Making: They can decide which tool is needed based on the user's question.
# 5. Dynamic Responses: They can observe tool results and decide what action to take next.