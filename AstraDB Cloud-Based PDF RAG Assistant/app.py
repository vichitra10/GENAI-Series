
from langchain_community.vectorstores import Cassandra
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os
import cassio
import hashlib
import json
import traceback

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq


# Load environment variables
load_dotenv()

ASTRA_DB_ID = os.getenv("ASTRA_DB_ID")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

PDF_PATH = "genai.pdf"
TABLE_NAME = "genai_pdf"
HASH_FILE = "pdf_hash.json"


# Validate credentials
if not ASTRA_DB_ID or not ASTRA_DB_APPLICATION_TOKEN:
    raise ValueError("Astra DB credentials are missing")

if not GROQ_API_KEY:
    raise ValueError("Groq API key is missing")


# Check PDF
if not os.path.exists(PDF_PATH):
    raise FileNotFoundError(f"PDF not found: {PDF_PATH}")


# Generate PDF fingerprint
def get_pdf_hash(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()


current_hash = get_pdf_hash(PDF_PATH)

# Check whether PDF has already been processed
previous_hash = None

if os.path.exists(HASH_FILE):
    with open(HASH_FILE, "r") as file:
        previous_hash = json.load(file).get("pdf_hash")


# Connect to Astra DB
cassio.init(
    token=ASTRA_DB_APPLICATION_TOKEN,
    database_id=ASTRA_DB_ID
)

print("Connected to Astra DB")


# HuggingFace embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


# Ingest PDF only when it is new or changed
if current_hash != previous_hash:

    print("New or updated PDF detected. Processing...")

    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    if not docs:
        raise ValueError("No content found in PDF")

    print("Total PDF pages:", len(docs))

    chunks = text_splitter.split_documents(docs)

    print("Total chunks:", len(chunks))

    # Add document identification metadata
    for chunk in chunks:
        chunk.metadata["document_id"] = PDF_PATH

    # Store embeddings in Astra DB
    astra_vector_store = Cassandra.from_documents(
        documents=chunks,
        embedding=embeddings,
        table_name=TABLE_NAME
    )

    # Save processed PDF hash
    with open(HASH_FILE, "w") as file:
        json.dump({"pdf_hash": current_hash}, file)

    print("PDF embeddings stored successfully!")

else:

    print("PDF already processed. Reusing existing records.")

    # Connect to the existing Cassandra table
    astra_vector_store = Cassandra(
        embedding=embeddings,
        table_name=TABLE_NAME
    )


# Create retriever
retriever = astra_vector_store.as_retriever(
    search_kwargs={"k": 3}
)


# Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# Prompt
prompt = PromptTemplate(
    template="""
    You are a PDF question-answering assistant.

    Answer using ONLY the provided context.

    Rules:
    1. Do not use outside knowledge.
    2. Do not make up information.
    3. If the answer is not available in the context,
       say:
       "I could not find this information in the provided PDF."
    4. Keep the answer clear and relevant.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """,
    input_variables=["context", "question"]
)


# LCEL chain
chain = prompt | llm | StrOutputParser()


# Question answering function
def ask_question(question):

    if not question.strip():
        return "Please enter a valid question."

    try:

        relevant_docs = retriever.invoke(question)

        if not relevant_docs:
            return "I could not find this information in the provided PDF."

        context = "\n\n".join(
            [doc.page_content for doc in relevant_docs]
        )

        answer = chain.invoke({
            "context": context,
            "question": question
        })

        print("\nSources:")

        for doc in relevant_docs:

            page = doc.metadata.get("page")

            # if page is not None:
            #     page += 1

            if page is not None:
            #    page = int(page) + 1
                 page = int(float(page)) + 1

            print(
                f"PDF: {doc.metadata.get('source', PDF_PATH)}, "
                f"Page: {page if page is not None else 'Unknown'}"
            )

        return answer

    except Exception as e:

        print("Error:", str(e))
        traceback.print_exc()

        return "Something went wrong while processing your question."


# Task 6: Testing
test_questions = [
    "What is AI exposure and complementarity?",
    "How does AI influence worker reallocation?",
    "What is the relationship between AI, productivity, and inequality?",
    "What factors are considered in AI preparedness?",
    "What are the policy considerations discussed in the report?"
]


for question in test_questions:

    print("\nQuestion:", question)

    answer = ask_question(question)

    print("Answer:", answer)


# Interactive question answering
while True:

    question = input("\nAsk your question (type exit to stop): ")

    if question.lower().strip() == "exit":
        break

    answer = ask_question(question)

    print("\nAnswer:", answer)





## Observation and Insights
# Q1. Why is Astra DB useful for production RAG?
# - Cloud-based vector database.
# - Stores document embeddings and metadata.
# - Supports scalable semantic search.
# - Provides persistent storage and retrieval.
# - Suitable for applications handling large amounts of documents.

# Q2. Importance of Session State in GenAI Applications
# - Maintains conversation history.
# - Remembers previous user interactions.
# - Supports multi-turn conversations.
# - Stores temporary user-specific data.
# - Helps provide context-aware responses.


# Q3. Difference between FAISS and Astra DB
# FAISS: FAISS (Facebook AI Similarity Search) is a vector search library used to perform similarity searches on high-dimensional vectors. It generally runs locally and is useful for building local RAG applications. It mainly focuses on efficient vector similarity search. Additional handling is required for persistent storage.

# Astra DB: Astra DB is a cloud-based database that supports vector storage and retrieval. It stores document embeddings along with metadata and supports semantic search. It provides persistent storage and is suitable for scalable, production-level RAG applications.