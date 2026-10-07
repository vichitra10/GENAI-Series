WikiPedia Retriever:  Wikipedia Retriever is a Retriever that fetches the relevant content from the (wikipedia api) for a given query

Vector Store Retriever: A langChain Vector Store Retriever is the most common type of Retriever that search and fetch the most relevant documents from a vector store based on semantic similiarty using the vector embedding.

How it works

Store the documents in a [vector-store] like FAISS, ChromaDB, Weaviate, AstraDB.
Each Documents is converted into a dense vector using en embedding vector
When the user enter the query , its also turns into a vector .
The Retriever compares the query vector with the stored vectors.
It retruved the top k most similiar results.



Different type of Retriever
Maximal Marginal Relevance Retriever: It is an Information-Reterival-Algo designed to reduce redundancy in the Reterived Data while maintaining High relevance to the query.
Why do we require this MMR Retriever

In regular similarity search, the retrieved documents are likely to be very similar to each other. They may contain repeated or overlapping information because the search focuses mainly on finding documents that are most similar to the query.


Multi Query Retriever: Multi-Query Retriever is a retrieval technique in RAG where the user's single query is converted into multiple different queries. Each query is used to retrieve documents, and the results are combined.

Why do we need it?

A user may ask a question in only one way, but the information in our documents may be written using different words.

For example:

User Query:
"What are the benefits of solar energy?"

A Multi-Query Retriever might generate:

Query 1: What are the advantages of solar power?
Query 2: How does solar energy benefit the environment?
Query 3: Why is solar power considered a renewable energy source?

Contextual Compression Retriever
Contextual Compression Retriever is a retriever that retrieves documents first and then removes the unnecessary parts of those documents, keeping only the information relevant to the user's query.


User Query
   ↓
Vector Store
   ↓
Retrieve Documents
   ↓
Compression / Filtering
   ↓
Keep only relevant information
   ↓
Return compressed documents


