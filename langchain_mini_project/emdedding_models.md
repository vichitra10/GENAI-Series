Embedding Models: An Embedding Model converts (text, word , sentences, document) into a list of numbers. 
Each Vectors capture the semantic meaning of the text.
In LangChain Embedding are used for search , reterival, clustering , classification & Recommandation. 

Embeddings are a way of turning Language into math , so that computer can compare meaning. 


Why do we need the Embeddings:
1) Find similiar text for Semantic Search
2) Reterive Relevant chunks from the large data
3) Detect clusetrs or Duplicate



PDF / Website / Document
        ↓
Document Loader
        ↓
Text Splitter
        ↓
Chunks
        ↓
Embeddings ⭐
        ↓
Vector Database
        ↓
Retriever
        ↓
Relevant Chunks
        ↓
LLM
        ↓   
Answer


