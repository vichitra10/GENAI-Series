import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from langchain_classic.chains import (
    create_retrieval_chain,
    create_history_aware_retriever
)
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain
)

load_dotenv()

st.title("RAG Chatbot")
st.write("Upload a PDF or text file and ask questions about its content.")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "processed_file" not in st.session_state:
    st.session_state.processed_file = None


# Initialize the model
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# File uploader
uploaded_file = st.file_uploader(
    "Upload a PDF or text file",
    type=["pdf", "txt"]
)


# Process uploaded document
if uploaded_file is not None:
    if st.button("Process Document"):
        try:
            with st.spinner("Loading document..."):

                if uploaded_file.name.lower().endswith(".pdf"):
                    temp_path = None

                    try:
                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=".pdf"
                        ) as temp_file:
                            temp_file.write(uploaded_file.getvalue())
                            temp_path = temp_file.name

                        documents = PyPDFLoader(temp_path).load()

                    finally:
                        if temp_path and os.path.exists(temp_path):
                            os.remove(temp_path)

                else:
                    text = uploaded_file.getvalue().decode("utf-8")

                    if not text.strip():
                        raise ValueError("The text file is empty.")

                    documents = [
                        Document(
                            page_content=text,
                            metadata={"source": uploaded_file.name}
                        )
                    ]

                # Check document content
                if not documents or not any(
                    doc.page_content.strip() for doc in documents
                ):
                    raise ValueError("No readable text was found.")

                # Split documents
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )

                chunks = splitter.split_documents(documents)

                if not chunks:
                    raise ValueError("No text chunks could be created.")

            # Create embeddings and vector store
            with st.spinner("Creating embeddings and vector store..."):
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )

                new_vector_store = FAISS.from_documents(
                    chunks,
                    embedding=embeddings
                )

            # Update state only after successful processing
            st.session_state.vector_store = new_vector_store
            st.session_state.processed_file = uploaded_file.name
            st.session_state.messages = []

            st.success(
                f"Successfully processed {uploaded_file.name}"
            )

        except Exception as e:
            st.error("Unable to process this document.")
            st.caption(f"Error details: {e}")


# Show processed document status
if st.session_state.vector_store is not None:
    st.info(
        f"Active document: {st.session_state.processed_file}"
    )


# Display previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
user_question = st.chat_input(
    "Ask a question about your document"
)


if user_question:

    if st.session_state.vector_store is None:
        st.warning("Please upload and process a document first.")

    else:
        # Save and display user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("user"):
            st.markdown(user_question)

        try:
            # Convert previous Streamlit messages to LangChain messages
            chat_history = []

            for message in st.session_state.messages[:-1]:
                if message["role"] == "user":
                    chat_history.append(
                        HumanMessage(content=message["content"])
                    )
                else:
                    chat_history.append(
                        AIMessage(content=message["content"])
                    )

            # Prompt to rewrite follow-up questions
            contextualize_prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    """Given the conversation history and the latest
                    question, rewrite the latest question as a standalone
                    question that can be understood without the history.
                    Do not answer the question."""
                ),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ])

            # Prompt to answer using retrieved document context
            prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    """Answer the question using only the provided
                    document context.

                    Use the conversation history to understand
                    follow-up questions.

                    If the answer is not available in the document
                    context, say:
                    "I don't know based on the provided context."

                    Context:
                    {context}"""
                ),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}")
            ])

            # Create retriever
            retriever = st.session_state.vector_store.as_retriever(
                search_kwargs={"k": 3}
            )

            # Make retrieval aware of conversation history
            history_aware_retriever = create_history_aware_retriever(
                llm,
                retriever,
                contextualize_prompt
            )

            # Create question-answer chain
            question_answer_chain = create_stuff_documents_chain(
                llm,
                prompt
            )

            # Create complete RAG chain
            rag_chain = create_retrieval_chain(
                history_aware_retriever,
                question_answer_chain
            )

            # Generate answer
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = rag_chain.invoke({
                        "input": user_question,
                        "chat_history": chat_history
                    })

                    answer = response["answer"]
                    st.markdown(answer)

            # Save assistant response after success
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(
                "Sorry, I couldn't generate an answer. "
                "Please try again."
            )
            st.caption(f"Error details: {e}")



## Task 11: Observation and insights
## Q.1: Why RAG is suitable for RAG Chatbots
## Ans: RAG is suitable for chatbots because it retrieves relevant information from documents and uses it to generate accurate, context-based answers. It supports follow-up questions, reduces hallucinations, and allows updated information to be used without retraining the LLM.

## Q.2: Difference between GROQ RAG and OpenAI RAG
## Ans: Both retrieve relevant document information and use an LLM to generate answers. The main differences are model capabilities, speed, pricing, and API limits.
## Groq RAG: Uses Groq models.
## OpenAI RAG: Uses OpenAI models.

## Q.3: Role of Streamlit in rapid GenAI prototyping
## Ans: Streamlit helps rapidly build interactive web interfaces for GenAI applications using Python, with minimal frontend code. It lets developers quickly test and demonstrate features like chatbots, file uploads, RAG, and LLM responses.


