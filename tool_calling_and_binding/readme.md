# GEN_AI Python Assignment 32

## Name
Vichitra Saini

## Topic
Tools, Tool Calling and ReAct Agents using LangChain

## Tasks Completed

### Part 1: Tools in AI Agents
- **Task 1:** Understanding Tools (Conceptual)
- **Task 2:** Built-in Tools in LangChain (Calculator, Wikipedia, Web Search)

### Part 2: Creating Custom Tools and Toolkit
- **Task 3:** Create a Custom Tool (`company_policy_lookup`)
- **Task 4:** Create a Custom Toolkit (policy lookup, database query, date/time)

### Part 3: Tool Binding and Tool Calling
- **Task 5:** Tool Binding to LLM
- **Task 6:** Tool Calling Flow (single-tool and multi-tool queries)

### Part 4: Creating a ReAct AI Agent
- **Task 7:** ReAct Agent Overview (Conceptual)
- **Task 8:** Build a ReAct Agent (ReAct prompt, tools, Think / Act / Observe / Answer)
- **Task 9:** Testing the ReAct Agent (factual, calculation, multi-step)

### Part 5: Mini Project: AI Agent Assistant
- **Task 10:** Agent Use Case (answer questions, perform calculations, retrieve information, automatic tool selection)
- **Task 11:** Observation and Insights

## Language
- Python 3

## Technologies Used
- Python
- langchain
- langchain-classic
- langchain-core
- langchain-community
- langchain-experimental
- langchain-groq
- langchain-google-genai
- langsmith
- wikipedia
- duckduckgo-search
- ddgs
- numexpr
- python-dotenv

## Project Structure

```text
GEN_AI_Assignment_32/
│
├── app.ipynb             # Task 1 to Task 3 (concepts, built-in tools, custom tool)
├── custom_toolkit.py     # Task 4  (custom toolkit)
├── tool_binding.py       # Task 5  (bind tools to the LLM)
├── tool_calling.py       # Task 6  (tool calling flow)
├── react_agent.py        # Task 7 to Task 11 (ReAct agent, testing, mini project)
│
├── requirements.txt      # Required Python dependencies
├── .env                  # Groq API key (keep private)
└── README.md             # Project documentation
```

## How to Run

### 1. Download the Project

Download the project to your local system and open the project folder in VS Code.

### 2. Install Dependencies

Make sure Python 3 is installed. Create and activate a virtual environment (recommended), then run:

```bash
pip install -r requirements.txt
```

`requirements.txt` should contain:

```text
langchain
langchain-classic
langchain-core
langchain-community
langchain-experimental
langchain-groq
langchain-google-genai
langsmith
wikipedia
duckduckgo-search
ddgs
numexpr
python-dotenv
```

### 3. Configure the API Key

Create a `.env` file in the project directory and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your actual API key.

**Important:** Keep your API key private. Do not upload your `.env` file to GitHub.

### 4. Run Each Part

| Tasks | How to run |
|---|---|
| Task 1 to 3 | Open `app.ipynb` and run all cells |
| Task 4 | `python custom_toolkit.py` |
| Task 5 | `python tool_binding.py` |
| Task 6 | `python tool_calling.py` |
| Task 7 to 11 | `python react_agent.py` (shows a menu) |

`react_agent.py` also accepts a mode directly:

```bash
python react_agent.py test    # Task 9: run the three test questions
python react_agent.py chat    # Task 10: start the AI Agent Assistant
```

### 5. Use the AI Agent Assistant (Task 10)

1. Run `python react_agent.py chat`.
2. Type a question, for example:
   - `Who invented the World Wide Web and in which year?` (Wikipedia)
   - `What is 15% of 2480, plus 125?` (calculator)
   - `In which year was the Eiffel Tower completed, and how many years ago was that?` (Wikipedia, date tool and calculator)
   - `How many days of notice do I need before resigning?` (company policy tool)
3. Watch the reasoning trace printed in the terminal (Thought, Action, Action Input, Observation, Final Answer).
4. The agent chooses the tools automatically. Type `exit` to quit.

## ReAct Agent Overview

ReAct (Reasoning + Acting) lets an LLM solve a question in a loop instead of answering in one shot:

```text
Question      : What is 15% of 2480, plus 125?
Thought       : I need to calculate this, so I should use the calculator.
Action        : calculator
Action Input  : 0.15 * 2480 + 125
Observation   : 497.0
Thought       : I now know the final answer.
Final Answer  : 497
```

| Step | Meaning |
|---|---|
| Think | The LLM reasons about what to do next |
| Act | The LLM picks a tool and writes its input |
| Observe | The tool runs and returns a result |
| Answer | When enough information is gathered, the LLM writes the final answer |

### Tools available to the agent

| Tool | Purpose |
|---|---|
| `wikipedia` | Facts about people, places, events and concepts |
| `calculator` | All arithmetic (built on `numexpr`) |
| `duckduckgo_search` | Recent news and web information |
| `current_datetime` | Today's date, day and time |
| `company_policy_lookup` | Company policies (mock data) |

## Notes

- Tasks 1 to 3 are in a notebook. Tasks 4 to 6 are separate scripts. Tasks 7 to 11 are in one file, `react_agent.py`.
- The ReAct prompt is a custom template with the placeholders `{tools}`, `{tool_names}`, `{input}` and `{agent_scratchpad}`.
- The agent is built with `create_react_agent` and run by `AgentExecutor`.
- `verbose=True` prints the full reasoning trace, and `return_intermediate_steps=True` lets the script print a step summary after each question.
- `max_iterations` limits the Think / Act / Observe cycles so the agent cannot loop forever.
- `handle_parsing_errors=True` lets the agent recover when the LLM breaks the ReAct format.
- A ReAct agent passes tool input as plain text, so every tool takes a single string.
- The LLM used is `llama-3.3-70b-versatile` on Groq with `temperature=0`.
- Tasks 5 and 6 use native tool calling (`bind_tools` and `tool_calls`). Task 8 onwards uses text-based ReAct.
- Configure a valid Groq API key before running any script.
- Package versions can be pinned in `requirements.txt` for improved reproducibility.

