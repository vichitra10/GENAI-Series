# GEN_AI Python Assignment 36

## Name
Vichitra Saini

## Topic
HuggingFace & LangChain Integration (Using Groq ChatModel)

## Tasks Completed

### Part 1: Getting Started with AstraDB (DataStax)
- **Task 1:** Initialize Groq ChatModel using LangChain.
- **Task 2:** Connect LangChain with AstraDB
- **Task 3:** Load and Split PDF Documents
- **Task 4:** Store Embeddings in AstraDB
- **Task 5:** PDF Query RAG Application
- **Task 6:** Testing and Validation
- **Task 7:** Observations and Insights




## Language
- Python 3

## Technologies Used
- Python
- LangChain
- LangChain Core
- LangChain Groq
- Groq API
- PromptTemplate
- ChatPromptTemplate
- LCEL (LangChain Expression Language)

## Project Structure

```text
GEN_AI_HuggingFace_LangChain/
│
├── app.py                  # All assignment tasks
├── requirements.txt        # Required Python dependencies
├── .env                    # Groq API key (keep private)
└── README.md               # Project documentation
```

## How to Run

### 1. Download the Project

Download the project to your local system and open the project folder in VS Code.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate
```

### 3. Install Dependencies

Run the following command:

```bash
pip install -r requirements.txt
```

`requirements.txt` should contain:

```text
langchain
langchain-core
langchain-groq
python-dotenv
```

### 4. Configure the API Key

Create a `.env` file in the project directory and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your actual Groq API key.

Get your API key from:

https://console.groq.com/keys

**Important:** Keep your API key private. Do not upload your `.env` file to GitHub.

### 5. Run the Application

Execute the following command:

```bash
python app.py
```

## Concepts Covered

### 1. Groq ChatModel
- Initialize a hosted AI model using ChatGroq.
- Configure model parameters such as temperature.
- Generate responses using `invoke()`.

### 2. PromptTemplate
- Create reusable prompt templates.
- Pass dynamic input variables.
- Connect prompts with the model using LCEL.

### 3. ChatPromptTemplate
- Create structured chat prompts.
- Use system and human messages.
- Generate conversational responses.

### 4. LCEL (LangChain Expression Language)

Connect prompts and models using the pipe operator:

```python
chain = prompt | llm
```

This creates a chain where the formatted prompt is passed to the language model.

## Comparison: PromptTemplate vs ChatPromptTemplate

| Feature | PromptTemplate | ChatPromptTemplate |
|---|---|---|
| Input format | Single text prompt | Multiple messages |
| System message | Not separately structured | Supported |
| Human message | Not separately structured | Supported |
| Usage | Simple LLM applications | Chat applications |

## Notes

- All assignment tasks are implemented in a single `app.py` file.
- Groq ChatModel is used instead of Hugging Face models.
- The model used is `openai/gpt-oss-20b`.
- Groq API is used for cloud-based model inference.
- No model downloading is required.
- PromptTemplate and ChatPromptTemplate are implemented using LangChain Core.
- LCEL is used to connect prompts with the model.
- A valid Groq API key is required to execute the application.

## Conclusion

This assignment demonstrates how to integrate a hosted AI model with LangChain using Groq ChatModel. It covers model initialization, prompt engineering, reusable prompt templates, structured chat messages, and LCEL-based chains.

The practical implementation helps understand how language models can be integrated into GenAI applications using LangChain.
