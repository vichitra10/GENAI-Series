## Task 4 : Create a Custom Toolkit

import os
from dotenv import load_dotenv
load_dotenv()

from groq import Groq
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.agents import create_react_agent, AgentExecutor
from langsmith import Client
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import load_tools
from langchain_classic.chains.llm_math.prompt import PROMPT
from langchain_core.tools import tool, BaseTool, BaseToolkit
import numexpr
import wikipedia.wikipedia as wp_mod
import sqlite3
from datetime import datetime
from typing import List

wp_mod.USER_AGENT = "Assignment32Bot/1.0 (vichi.techsaga@gmail.com)"

# ---------------------------------------------------------------
# Mock data: policies + in-memory SQLite database
# ---------------------------------------------------------------
POLICIES = {
    "leave": "Employees get 24 paid leaves per year. Submit requests 3 days in advance.",
    "work from home": "Work from home is allowed up to 2 days per week with manager approval.",
    "working hours": "Working hours are 9:30 AM to 6:30 PM, Monday to Friday.",
    "dress code": "Business casual Monday to Thursday, casual on Fridays.",
    "notice period": "The standard notice period for resignation is 60 days.",
}

conn = sqlite3.connect(":memory:", check_same_thread=False)
conn.execute(
    "CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, "
    "department TEXT, salary INTEGER)"
)
conn.executemany(
    "INSERT INTO employees VALUES (?, ?, ?, ?)",
    [
        (1, "Aarav Sharma", "Engineering", 90000),
        (2, "Priya Verma", "HR", 60000),
        (3, "Rohan Mehta", "Engineering", 85000),
        (4, "Sneha Iyer", "Finance", 70000),
        (5, "Kabir Singh", "Marketing", 65000),
    ],
)
conn.commit()


# ---------------------------------------------------------------
# Individual tools
# ---------------------------------------------------------------
@tool
def policy_lookup(query: str) -> str:
    """Return company policy information (leave, work from home,
    working hours, dress code, notice period)."""
    q = query.lower()
    for keyword, policy in POLICIES.items():
        if keyword in q:
            return policy
    return f"No policy found. Available topics: {', '.join(POLICIES)}."


@tool
def database_query(sql: str) -> str:
    """Run a read-only SQL SELECT query on the employees table
    (columns: id, name, department, salary) and return the rows."""
    if not sql.strip().lower().startswith("select"):
        return "Error: only SELECT queries are allowed."
    try:
        rows = conn.execute(sql).fetchall()
        return str(rows) if rows else "No rows found."
    except sqlite3.Error as e:
        return f"SQL error: {e}"


@tool
def datetime_tool(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Return the current date and time. Optionally pass a strftime format,
    e.g. '%A, %d %B %Y' for the weekday and full date."""
    try:
        return datetime.now().strftime(fmt)
    except ValueError as e:
        return f"Invalid format: {e}"


# ---------------------------------------------------------------
# Step 1: Group the tools into a toolkit
# ---------------------------------------------------------------
class CompanyToolkit(BaseToolkit):
    """A toolkit that bundles company-related tools."""

    def get_tools(self) -> List[BaseTool]:
        return [policy_lookup, database_query, datetime_tool]


# ---------------------------------------------------------------
# Step 2: Test the toolkit
# ---------------------------------------------------------------
if __name__ == "__main__":
    toolkit = CompanyToolkit()
    tools = toolkit.get_tools()

    print("Tools in toolkit:")
    for t in tools:
        print(f"  - {t.name}: {t.description.splitlines()[0]}")

    tool_map = {t.name: t for t in tools}

    print("\n---- Policy Lookup")
    print(tool_map["policy_lookup"].invoke("What is the leave policy?"))

    print("\n---- Database Query")
    print(tool_map["database_query"].invoke(
        "SELECT name, salary FROM employees WHERE department = 'Engineering'"
    ))
    print(tool_map["database_query"].invoke("DELETE FROM employees"))  # blocked

    print("\n---- Date/Time")
    print(tool_map["datetime_tool"].invoke({}))
    print(tool_map["datetime_tool"].invoke({"fmt": "%A, %d %B %Y"}))

    