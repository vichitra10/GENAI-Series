
from pathlib import Path
from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent
)
from langchain_classic.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import StructuredTool
from sqlalchemy import create_engine, inspect
from urllib.parse import quote_plus
from dotenv import load_dotenv
import sqlite3
import os


load_dotenv()

# ==========================================
# TASK 1: CREATE SQLITE DATABASE
# ==========================================

# Step 1: Create database connection
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Step 2: Create employees table
conn.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary INTEGER
)
""")

# Step 3: Create sales table
conn.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    amount INTEGER,
    sale_date TEXT
)
""")

print("Database and tables created successfully!")

# Clear existing records to avoid duplicate IDs
cursor.execute("DELETE FROM sales")
cursor.execute("DELETE FROM employees")

# Step 4: Insert employees data
employees = [
    (1, 'Rahul', 'IT', 45000),
    (2, 'Priya', 'HR', 40000),
    (3, 'Amit', 'Sales', 50000),
    (4, 'Neha', 'IT', 55000),
    (5, 'Rohit', 'Finance', 48000),
    (6, 'Sneha', 'HR', 42000),
    (7, 'Karan', 'Sales', 52000),
    (8, 'Pooja', 'IT', 60000),
    (9, 'Arjun', 'Finance', 47000),
    (10, 'Simran', 'Sales', 53000)
]

cursor.executemany(
    "INSERT INTO employees VALUES (?, ?, ?, ?)",
    employees
)

# Step 5: Insert sales data
sales = [
    (1, 1, 15000, '2026-01-01'),
    (2, 2, 20000, '2026-01-02'),
    (3, 3, 25000, '2026-01-03'),
    (4, 4, 18000, '2026-01-04'),
    (5, 5, 30000, '2026-01-05'),
    (6, 6, 12000, '2026-01-06'),
    (7, 7, 22000, '2026-01-07'),
    (8, 8, 35000, '2026-01-08'),
    (9, 9, 17000, '2026-01-09'),
    (10, 10, 28000, '2026-01-10')
]

cursor.executemany(
    "INSERT INTO sales VALUES (?, ?, ?, ?)",
    sales
)

# Step 6: Save changes
conn.commit()

# Step 7: Verify employees
cursor.execute("SELECT * FROM employees")
print("\nEmployees:")
for row in cursor.fetchall():
    print(row)

# Step 8: Verify sales
cursor.execute("SELECT * FROM sales")
print("\nSales:")
for row in cursor.fetchall():
    print(row)

# Step 9: Close SQLite connection
conn.close()

print("\nData inserted successfully!")

# Step 10: Create SQLAlchemy engine
engine = create_engine("sqlite:///company.db")

# Step 11: Test database connection
with engine.connect() as connection:
    print("\nSQLite Database connected successfully!")

# Step 12: Fetch table names
inspector = inspect(engine)
tables = inspector.get_table_names()

print("Available SQLite tables:", tables)


# ==========================================
# TASK 2/3: CONNECT TO MYSQL WORKBENCH
# ==========================================

# Step 1: Create SQLDatabase object using MySQL

MYSQL_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD", "user@123"))

mysql_uri = (
    f"mysql+mysqlconnector://root:{MYSQL_PASSWORD}"
    "@127.0.0.1:3307/company_db"
)

db = SQLDatabase.from_uri(mysql_uri)

print("\nMySQL Database connected successfully!")


# ==========================================
# TASK 4: INITIALIZE GROQ LLM
# ==========================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================
# TASK 5: INITIALIZE SQL TOOLKIT
# ==========================================

# Step 1: Create MySQL Toolkit
mysql_toolkit = SQLDatabaseToolkit(
    db=db,
    llm=llm
)

# Step 2: Get available SQL tools
mysql_tools = mysql_toolkit.get_tools()

print("\nAvailable MySQL SQL Toolkit Tools:")

for tool in mysql_tools:
    print("\nTool Name:", tool.name)
    print("Description:", tool.description)

# Step 3: Test SQL Query Tool
query_tool = next(
    tool for tool in mysql_tools
    if tool.name == "sql_db_query"
)

result = query_tool.invoke({
    "query": "SELECT * FROM employees LIMIT 5;"
})

print("\nMySQL SQL Query Result:")
print(result)

# Step 4: Test Table Information Tool
schema_tool = next(
    tool for tool in mysql_tools
    if tool.name == "sql_db_schema"
)

schema = schema_tool.invoke({
    "table_names": "employees"
})

print("\nMySQL Employees Table Information:")
print(schema)


# ==========================================
# TASK 6: CREATE SQL AGENT
# ==========================================

# Step 1: Create SQLite Database Object

sqlite_db = SQLDatabase.from_uri(
    "sqlite:///company.db"
)

print("\nSQLite SQLDatabase object created successfully!")


# Step 2: Create SQLite SQL Toolkit

sqlite_toolkit = SQLDatabaseToolkit(
    db=sqlite_db,
    llm=llm
)

sqlite_tools = sqlite_toolkit.get_tools()


# Step 3: Create separate tool names for both databases

def create_prefixed_tool(tool, database_name):

    def run_tool(**kwargs):
        return tool.invoke(kwargs)

    return StructuredTool.from_function(
        func=run_tool,
        name=f"{database_name}_{tool.name}",
        description=(
            f"Use this tool only for the {database_name} database. "
            f"{tool.description}"
        ),
        args_schema=tool.args_schema
    )


# Step 4: Combine SQLite and MySQL tools

agent_tools = []

for tool in sqlite_tools:
    agent_tools.append(
        create_prefixed_tool(tool, "sqlite")
    )

for tool in mysql_tools:
    agent_tools.append(
        create_prefixed_tool(tool, "mysql")
    )

print("\nTotal SQL Agent Tools:", len(agent_tools))

print("\nAvailable SQL Agent Tools:")

for tool in agent_tools:
    print(tool.name)


# Step 5: Create Agent Prompt

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a SQL database assistant.

        You have access to two databases:

        1. SQLite database: company.db
        2. MySQL database: company_db

        Select the correct database tools based on
        the user's question.

        Use SQLite tools for SQLite database questions.

        Use MySQL tools for MySQL database questions.

        Do not mix records from the two databases.

        First check the available tables and their schemas
        when necessary.

        Generate appropriate SQL queries and provide
        clear answers based on the query results.
        """
    ),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])


# Step 6: Create SQL Agent

agent = create_tool_calling_agent(
    llm=llm,
    tools=agent_tools,
    prompt=prompt
)


# Step 7: Create Agent Executor

agent_executor = AgentExecutor(
    agent=agent,
    tools=agent_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)

print("\nSQL Agent created successfully!")


# Step 8: Test SQLite Database

print("\n========== SQLITE AGENT TEST ==========")

response = agent_executor.invoke({
    "input": "Show the names and salaries of all employees from the SQLite database."
})

print("\nSQLite Agent Response:")
print(response["output"])


# Step 9: Test MySQL Database

print("\n========== MYSQL AGENT TEST ==========")

response = agent_executor.invoke({
    "input": "List all available tables in the MySQL database."
})

print("\nMySQL Agent Response:")
print(response["output"])


print("\nTask 6: SQL Agent completed successfully!")


# ==============================
# TASK 7: CHAT WITH SQL DATABASE
# ==============================

print("\n========== TASK 7: CHAT WITH SQL DATABASE ==========")

questions = [
    "How many employees are there in each department in the SQLite database?",
    "Who has the highest salary in the MySQL database?",
    "What is the total sales amount in the SQLite database?",
    "What is the average salary per department in the MySQL database?"
]

# for question in questions:

#     print("\nQuestion:", question)

#     response = agent_executor.invoke({
#         "input": question
#     })

#     print("Answer:", response["output"])

for question in questions:

    print("\nQuestion:", question)

    try:
        response = agent_executor.invoke({
            "input": question
        })

        print("Answer:", response["output"])

    except Exception as e:
        print("Error:", e)


# ==============================
# TASK 8: HANDLING AMBIGUOUS QUERIES
# ==============================

print("\n========== TASK 8: HANDLING AMBIGUOUS QUERIES ==========")

ambiguous_questions = [
    "Show me the data.",
    "What is the average?",
    "Tell me the highest value.",
    "Give me employee details."
]

for question in ambiguous_questions:

    print("\nQuestion:", question)

    response = agent_executor.invoke({
        "input": question
    })

    print("Agent Response:", response["output"])




## Observations and Insights

## Q.1: Why SQL Agents are better than manual SQL generation
## Answer: SQL Agents automate the complete process of understanding a user's question, inspecting the database schema, generating SQL queries, executing them, and interpreting the results. They can handle multi-step tasks and may recover from query errors, reducing manual effort.

## Q.2: Difference between SQL Agent and RAG
## Ans: SQL Agents retrieve information from structured databases by generating and executing SQL queries. RAG retrieves relevant information from documents or knowledge bases using similarity search and provides context to the LLM. SQL Agents are suitable for numerical and structured data queries, while RAG is suitable for contextual questions based on documents.

## Q.3: Risks of allowing unrestricted SQL access
## Ans: Unrestricted SQL access can lead to data deletion, unauthorized access, privacy leaks, incorrect query execution, and database performance issues. These risks can be reduced by using read-only permissions, restricting accessible tables, validating queries, applying query limits, and requiring approval for sensitive operations.

