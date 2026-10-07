Text Splitter: They divide large documents into smaller chunks of text , Now these chunks can be used for embedding , semantic serach, and Rag Application. 

Context length: No of tokens which your LLM models can take as an input in one go.
Context window ---> Context input + context Output

LLM --> Context Length

## token can be changed according to the gpt model
GPT 3.5: 16k Tokens
GPT 4.0: 128K Token

So, if a document is too long :
LLM can't process it at once
Reterival becomes insuffiecint
Important context moght be lost

Text Splitters also helps us into downstream task:
Downstream task:
 ** Embedding : Short chunks (more accurate vectors)
This process can help us out to numeric format that machine can understand

We have different type of Text splitters
Length Based
Text-Structured Based
Semantic Meaning Based
Document Structured Based