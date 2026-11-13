"""
Task 7 : ReAct Agent Overview        (Conceptual)
Task 8 : Build a ReAct Agent        (prompt + tools + Think/Act/Observe/Answer)
Task 9 : Testing the ReAct Agent    (factual, calculation, multi-step)
Task 10: Mini Project - AI Agent Assistant (interactive, auto tool selection)

"""

## Q.1: What is ReAct (Reason + Act)
## Ans: ReAct (Reason + Act) is a technique used in AI Agents where an LLM first reasons about a user's question, decides which action or tool is needed, executes that tool, and uses the result to generate an answer.

## Reason: AI understands the user's question and decides what to do.
## Act: AI selects and calls a tool.
## Observe: AI receives the tool's result.
## Repeat: AI may use another tool if needed.
## Final Answer: AI generates the final response.

## Q.2: Why ReAct Agent are powerful
## Ans: ReAct Agents are powerful because they can reason, use tools, observe results, and take multiple actions instead of only generating text like a normal LLM.
# 5 Reasons why ReAct Agents are powerful
# 1. Tool Usage: They can use tools such as databases, calculators, APIs, and search engines.
# 2. Real-time Information: They can retrieve updated information using external tools instead of relying only on training data.
# 3. Multi-step Problem Solving: They can break complex questions into smaller tasks and execute them step by step.
# 4. Decision Making: They can decide which tool is needed based on the user's question.
# 5. Dynamic Responses: They can observe tool results and decide what action to take next.

import sys
from dotenv import load_dotenv
from datetime import datetime

from langchain_groq import ChatGroq

from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_google_genai import ChatGoogleGenerativeAI

try:
    from langchain_classic.agents import AgentExecutor, create_react_agent
except ImportError:  # older LangChain versions
    from langchain.agents import AgentExecutor, create_react_agent

# Wikipedia sometimes blocks the default User-Agent (the JSON error you saw)
try:
    import wikipedia.wikipedia as _wp
    _wp.USER_AGENT = "Assignment32Bot/1.0 (your_email@example.com)"
except Exception:
    pass


load_dotenv()


# ===============================================================
# TASK 8 - Step 1: Tools (each takes ONE plain-text input)
# ===============================================================

def clean_input(text: str) -> str:
    """The LLM sometimes keeps writing 'Thought: ... Final Answer: ...' right
    after 'Action Input:' (before seeing the Observation). Keep only the first
    line and cut anything from 'Thought:' / 'Observation:' onwards."""
    text = str(text).strip().splitlines()[0] if str(text).strip() else ""
    for marker in ("Thought:", "Observation:"):
        text = text.split(marker)[0]
    return text.strip().strip("`'\"").strip()


# --- Retrieve information: Wikipedia + Web search (built-in, wrapped) ---
_wiki = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1500)
)
_ddg = DuckDuckGoSearchRun()


@tool
def wikipedia(query: str) -> str:
    """Look up facts about people, places, events and concepts on Wikipedia.
    Input: a short topic or search phrase."""
    return _wiki.run(clean_input(query))


@tool
def duckduckgo_search(query: str) -> str:
    """Search the web for recent news or information Wikipedia may not have.
    Input: a short search query."""
    return _ddg.run(clean_input(query))


# --- Perform calculations ---
@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression and return the number.
    Input must be a pure math expression such as '0.15 * 2480 + 125'
    or '(25 * 4 + 10) / 5'. Use * for multiplication and ** for powers.
    Do not include words or units."""
    import numexpr
    try:
        cleaned = clean_input(expression).replace(",", "").replace("^", "**")
        return str(numexpr.evaluate(cleaned))
    except Exception as e:
        return f"Calculator error: {e}. Send a pure math expression."


# --- Retrieve information: today's date ---
@tool
def current_datetime(query: str = "") -> str:
    """Return today's date, day of the week and current time.
    The input is ignored, so pass any text such as 'now'."""
    return datetime.now().strftime("%A, %d %B %Y, %H:%M:%S")


# --- Retrieve information: company policies (mock data) ---
POLICIES = {
    "leave": "Employees get 24 paid leaves per year. Submit requests 3 days in advance.",
    "work from home": "Work from home is allowed up to 2 days per week with manager approval.",
    "working hours": "Working hours are 9:30 AM to 6:30 PM, Monday to Friday.",
    "dress code": "Business casual Monday to Thursday, casual on Fridays.",
    "notice period": "The standard notice period for resignation is 60 days.",
}


@tool
def company_policy_lookup(query: str) -> str:
    """Return internal company policy information. Use ONLY for questions
    about this company's leave, work from home, working hours, dress code
    or notice period."""
    q = clean_input(query).lower()
    for keyword, policy in POLICIES.items():
        if keyword in q:
            return policy
    return f"No policy found. Available topics: {', '.join(POLICIES)}."


tools = [wikipedia, calculator, duckduckgo_search, current_datetime, company_policy_lookup]


# ===============================================================
# TASK 8 - Step 2: ReAct-style prompt
# Placeholders: {tools}, {tool_names}, {input}, {agent_scratchpad}
# ===============================================================
REACT_TEMPLATE = """You are a smart AI assistant. Answer the question as best you can.
You have access to the following tools:

{tools}

Use EXACTLY the following format:

Question: the input question you must answer
Thought: think about what you need to do next
Action: the tool to use, must be one of [{tool_names}]
Action Input: the input for the tool (plain text only, no quotes or code fences)
Observation: the result returned by the tool
... (this Thought/Action/Action Input/Observation cycle can repeat several times)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Tool selection rules:
- wikipedia: facts about people, places, events, concepts.
- calculator: ANY arithmetic. Never calculate in your head.
- duckduckgo_search: recent news or things Wikipedia may not have.
- current_datetime: today's date or the current year.
- company_policy_lookup: this company's internal policies only.
- If no tool is needed, go straight to the Final Answer.
- Never invent tool results. After writing Action Input, STOP and wait for the
  Observation. Do not write a Final Answer in the same reply as an Action.

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(REACT_TEMPLATE)


# ===============================================================
# TASK 8 - Step 3: Create the agent and attach the tools
# ===============================================================
# llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, max_retries=5)
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    stop_sequence=["\nObservation", "\nThought:"],  # stop right after Action Input
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,                    # prints Thought / Action / Observation live
    handle_parsing_errors=True,      # recover if the LLM breaks the format
    max_iterations=8,                # safety limit on Think-Act-Observe cycles
    return_intermediate_steps=True,  # lets us print a step summary
)


def run(question: str) -> str:
    """Run the agent on one question and print the reasoning trace summary."""
    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("=" * 70)

    result = agent_executor.invoke({"input": question})

    print("\n--- Reasoning trace summary ---")
    steps = result["intermediate_steps"]
    if not steps:
        print("No tool used (answered from the LLM's own knowledge).")
    for i, (action, observation) in enumerate(steps, 1):
        print(f"Step {i}: Act     -> {action.tool}")
        print(f"        Input   -> {action.tool_input}")
        print(f"        Observe -> {str(observation)[:150]}")
    print(f"\nFINAL ANSWER: {result['output']}")
    return result["output"]


# ===============================================================
# TASK 9 - Testing the ReAct agent
# ===============================================================
def run_tests():
    print("\n######## TEST 1: Factual question (Wikipedia) ########")
    run("Use Wikipedia to find out who invented the World Wide Web and in which year.")

    print("\n######## TEST 2: Calculation-based question ########")
    run("What is 15% of 2480, plus 125?")

    print("\n######## TEST 3: Multi-step reasoning question ########")
    run("In which year was the Eiffel Tower completed, and how many years ago "
        "was that from the current year?")


# ===============================================================
# TASK 10 - Mini project: AI Agent Assistant
# ===============================================================
def chat():
    print("\n=== AI Agent Assistant ===")
    print("Ask me anything: facts, calculations, today's date, company policies.")
    print("The agent chooses the tools automatically. Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ("exit", "quit", "q"):
            print("Goodbye!")
            break
        if not question:
            continue
        try:
            run(question)
        except Exception as e:
            print(f"Agent error: {e}")


if __name__ == "__main__":
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else ""

    if not mode:
        print("1) Run Task 9 tests\n2) Start Task 10 assistant")
        mode = {"1": "test", "2": "chat"}.get(input("Choose 1 or 2: ").strip(), "")

    if mode == "test":
        run_tests()
    elif mode == "chat":
        chat()
    else:
        print("Invalid choice. Use: python react_agent_project.py test|chat")



## Task 11: Observations and Insights
##  Q.1: Benefits of Tool-Augmented Agents
##  Ans:   Agents can use external tools such as APIs, databases, calculators, and search engines.
## They can access updated information.
## They can solve complex, multi-step problems.
## They can automate tasks and make decisions based on tool results.  

## Q2. Challenges with Agents
## Ans: Tool selection can be incorrect.
## Agents may produce inaccurate results.
## Multiple tool calls can increase response time and cost.
## Tool execution may fail due to API errors or network issues.
## Debugging and managing agent workflows can be difficult. 

## Q.3: Difference Between Chains and Agents
## Ans: Chains: Chains follow a predefined sequence of steps to complete a task. They are best suited for fixed and predictable workflows.

## Agents: Agents dynamically decide which steps or tools to use based on the user's query. They are best suited for complex tasks that require decision-making and flexibility.
    

## Q.4: When to Use Agents Over RAG
## Ans: Use agents when a task requires multiple tools or actions.
# When the system needs to interact with APIs, databases, or external services.
# When the next action depends on previous results.
# When a task requires dynamic decision-making.