# GEN_AI Python Assignment 34 (Text Summarization using LangChain)

## Name
Vichitra Saini

## Topic
Tools, Tool Calling and ReAct Agents using LangChain

## Tasks Completed

### Part 1: Basic Text Summerisation using PromptTemplate
- **Task 1:** Load the prepare Text
- **Task 2:** Prompt Based Summerization
- **Task 3:** Prompt Variations


### Part 2: Stuff Summerization Chain 
- **Task 4:** Why Stuff Chain is Needed (Conceptual)
- **Task 5:** Implement Stuff Summarization Chain
- **Task 6:** Comparison with Prompt-Based Summary

### Part 3: Map-Reduce Summarization Chain
- **Task 7:** Why Map-Reduce is Needed (Conceptual)
- **Task 8:** Implement Map-Reduce Summarization Chain
- **Task 9:** Analyze Map Outputs (Optional)

### Part 4: Refine Summarization Chain
- **Task 10:** Understand Refine Chain (Conceptual)
- **Task 11:** Implement Refine Summarization Chain 
- **Task 12:** Comparison of All Summarization Methods

### Part 5: Mini Project : Document Summarizer
- **Task 13:** Build a Summarization Function
- **Task 14:** Observations and Insights 



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

