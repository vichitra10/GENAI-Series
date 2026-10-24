# GEN_AI Python Assignment 27

## Name
Vichitra Saini

## Tasks Completed

### Part 1: Messages and MessagePlaceHolder
- **Task 1:** Understanding Chat Messages (Conceptual) 
- **Task 2:** MessagePlaceholder Usage

### Part 2: Conversation Histroy Management
- **Task 3:** Basic Message History
- **Task 4:** Trimming Chat History

### Part 3: Q&A Chatbot with message History
- **Task 5:** Build Q&A Chatbot
- **Task 6:** Build Stateful ChatBot Application
 **Task 7:** Observation and Insights



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
├── message.ipynb        # Part 1  Tasks 1&2
├── message.py           # Part 2: Tasks 3&4&5
├── app.py               # Part 3: Tasks 5&6&7
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

1. **`groq_part_1.ipynb`** — Tasks 1–2
2. **`groq_part_2.ipynb`** — Tasks 3-4
3. **`main.py`** — Tasks 5–10: 

**`Run the app.py application using streamlit app: run`**

Select the Python environment where the dependencies are installed as your Jupyter kernel.

Run the cells sequentially from top to bottom and review the output for each task.

## Notes

- Install all required dependencies using `requirements.txt`.
- Ensure your Groq API key is configured correctly before running the notebooks.
- The RAG task uses simple keyword-based retrieval rather than embedding-based semantic search.
- Package versions can be pinned in `requirements.txt` to make the environment more reproducible.
