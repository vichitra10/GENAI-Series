# GEN_AI Python Assignment 25

## Name
Vichitra Saini

## Tasks Completed

### Part 1: Prompt Templates
- **Task 1:** PromptTemplate
- **Task 2:** ChatPromptTemplate & Message Templates

### Part 2: Structured Output Using Pydantic
- **Task 3:** Pydantic Output Schema
- **Task 4:** Validation and Error Handling

### Part 3: Chains in LangChain
- **Task 5:** Simple Chain
- **Task 6:** Conditional Chain
- **Task 7:** Parallel Chain

### Part 4: Runnables and LCEL
- **Task 8:** Runnable Basics
- **Task 9:** LCEL-Based RAG Chain
- **Task 10:** Observation and Insights

## Language
Python 3

## Technologies Used
- Python
- LangChain
- LangChain Core
- LangChain Groq
- Pydantic
- Python-dotenv
- Jupyter Notebook
- LangChain Expression Language (LCEL)

## Project Structure

```text
GEN_AI_Assignment_25/
│
├── prompt_temp.ipynb    # Part 1 & 2: Tasks 1–4
├── chains.ipynb         # Part 3: Tasks 5–7
├── Runnable.ipynb       # Part 4: Tasks 8–10
├── requirements.txt     # Python dependencies
├── .env                 # Groq API key
└── README.md
```

## How to Run

### 1. Clone or Download the Project

Download the project to your local system and open its folder in VS Code or Jupyter Notebook.

### 2. Install Dependencies

Make sure Python 3 is installed. Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### 3. Configure the API Key

Create a `.env` file in the project directory and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your actual API key.

**Important:** Keep your API key private. Do not upload your `.env` file to GitHub.

### 4. Run the Jupyter Notebooks

Open the notebooks in the following order:

1. **`prompt_temp.ipynb`** — Tasks 1–4: Prompt Templates and Structured Output.
2. **`chains.ipynb`** — Tasks 5–7: Simple, Conditional, and Parallel Chains.
3. **`Runnable.ipynb`** — Tasks 8–10: Runnables, LCEL-Based RAG Chain, and Observations.

Select the Python environment where the dependencies are installed as your Jupyter kernel.

Run the cells sequentially from top to bottom and review the output for each task.

## Notes

- Install all required dependencies using `requirements.txt`.
- Ensure your Groq API key is configured correctly before running the notebooks.
- The RAG task uses simple keyword-based retrieval rather than embedding-based semantic search.
- Package versions can be pinned in `requirements.txt` to make the environment more reproducible.
