# GEN_AI Python Assignment 33

## Name
Vichitra Saini

## Topic
Tools, Tool Calling and ReAct Agents using LangChain

## Tasks Completed

### Part 1: Storing Data in Sqlite Database
- **Task 1:** Create Sqlite Database
- **Task 2:** Insert Sample Data

### Part 2: Creating LangChain Database Engine 
- **Task 3:** Create SQLAIChemy Engine
- **Task 4:** Create LangChain SQLDataBase Object

### Part 3: Connecting to Mysql Workbench
- ** Create a SQL Workbench Database to store Data
- ** Connect this SQL Workbench Database with code

### Part 4: Langchain SQL Toolkit and Agent
- **Task 5:** Initialize SQL Toolkit
- **Task 6:** Create SQL Agent
- **Task 7:** Chat with SQL Database

### Part 5: Agent Safety and Behaviour
- **Task 8:** Handling Ambiguous Queries
- **Task 9:** Observation and Insights  

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
GEN_AI_Assignment_33/
│
├── app.ipynb             
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

```bash
python app.py   

```

