What is RAG

RAG stands for Retrieval-Augmented Generation.
It is a technique where an LLM retrieves relevant information from an external knowledge source and then uses that information to generate an answer.

Simple example

Suppose you have a company document:

The company provides 20 days of annual leave.
Employees can apply for leave through the HR portal.

User asks:

How many annual leave days does the company provide?

Instead of relying only on what the LLM already knows, RAG does:
User Question
      ↓
   Retrieval
      ↓
Find relevant company document
      ↓
   Context
      ↓
      LLM
      ↓
   Final Answer

   The answer would be:

The company provides 20 days of annual leave.

Documents
   ↓
Document Loader
   ↓
Text Splitter
   ↓
Embeddings
   ↓
Vector Database
   ↓
Retriever
   ↓
Relevant Documents
   ↓
LLM
   ↓
Answer

Why do we use RAG?

An LLM has limitations:

Its training knowledge may not contain your private documents.
Its knowledge may not include recent information.
It can sometimes generate incorrect information.

RAG allows the application to retrieve information from an external source at query time and provide that information to the LLM as context.

RAG vs normal LLM
Normal LLM:

Question → LLM → Answer

RAG:
Question
   ↓
Search Knowledge Base
   ↓
Relevant Information
   ↓
LLM
   ↓
Answer

RAG connects an LLM with external knowledge so that the model can retrieve relevant information before generating an answer.


Youtube ChatBot (RAG Application )