# GEN_AI Python Assignment 30

## Name
Vichitra Saini

## Tasks Completed

### Part 1: GROQ Setup and Basic Chat
- **Task 1:** ChatGroq Setup
- **Task 2:** Basic Chat with ChatGroq

### Part 2: RAG Backend Pipeline
- **Task 3:** Document Loading and Text Splitting
- **Task 4:** Embedding and Vector Store
- **Task 5:** RAG Prompt Template

### Part 3: ChatGroq RAG Chain
- **Task 6:** Build RAG Chain

### Part 4: Streamlit UI
- **Task 7:** Build Streamlit Chat Interface
- **Task 8:** Integrate RAG Backend with UI

### Part 5: Testing and Validation
- **Task 9:** Multi-turn Chat Testing

### Part 6: Mini Project Deliverable
- **Task 10:** Final ChatGroq RAG App
- **Task 11:** Observations and Insights

## Language
- Python 3

## Technologies Used
- Python
- Streamlit
- LangChain
- LangChain Core
- LangChain Classic
- LangChain Groq
- Hugging Face Embeddings
- FAISS Vector Store
- PyPDFLoader
- Recursive Character Text Splitter
- Python-dotenv
- Groq API
- Retrieval-Augmented Generation (RAG)
- Conversation History and Streamlit Session State

## Project Structure

```text
GEN_AI_Assignment_30/
│
├── app.py             # Main Streamlit RAG chatbot application
├── requirements.txt   # Required Python dependencies
├── .env               # Groq API key (keep private)
└── README.md          # Project documentation
```

## How to Run

### 1. Clone or Download the Project

Download the project to your local system and open the project folder in VS Code.

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

### 4. Run the Streamlit Application

Run the following command from the project directory:

```bash
python -m streamlit run app.py
```

Open the application in your browser at:

`http://localhost:8501`

### 5. Use the RAG Chatbot

1. Upload a PDF or text file.
2. Click **Process Document** to load and process the document.
3. The application splits the text into chunks, creates embeddings, and stores them in FAISS.
4. Enter questions in the chat input.
5. Ask follow-up questions to test conversation history.
6. Review the answers generated using the retrieved document context.

## Notes

- The application is implemented in a single Python file, `app.py`.
- Install the required packages using `requirements.txt`.
- Configure a valid Groq API key before running the application.
- Hugging Face embeddings and FAISS are used for document retrieval.
- LangChain manages the retrieval and answer-generation pipeline.
- Streamlit session state maintains the conversation history during the active session.
- The chatbot uses retrieved document context to answer questions and is instructed to indicate when the answer is not available in the context.
- Package versions can be pinned in `requirements.txt` for improved reproducibility.
