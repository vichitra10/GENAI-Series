import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.summarize import load_summarize_chain

load_dotenv()

## Initialize LLM
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
    )


## Task 1: Load and Prepare Text
loader = PyPDFLoader("data/genai.pdf")
documents = loader.load()

text = "\n".join(doc.page_content for doc in documents)

print("\n========== TASK 1: DOCUMENT DETAILS ==========")

print("Total Characters:", len(text))

print("\nSample Content Preview:\n")
print(text[:1000]) ## starting 1000 chars


## Split document into chunks
text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
                )

chunks = text_splitter.split_documents(documents)
print("\nTotal Chunks:", len(chunks))


## Task 2:  Basic Summarization
summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    You are an expert text summarizer.
    Summarize the following text by identifying its important information and main ideas

    Text:
    {text}

    Summary:
    """
)

summary_chain = summary_prompt | model
response = summary_chain.invoke({
    "text": text[:10000]
})

print("\n Generated Summary:\n")
# print(response.content)


## Task 3 : Prompt Variations

short_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
    You are an expert text summarizer.

    Summarize the following text in 5-6 lines.
    Include only the most important information.

    Text:
    {text}

    Short Summary:
    """
)

short_chain = short_prompt | model

short_response = short_chain.invoke({
    "text": text[:10000]
})

print("\nShort Summary (5-6 Lines):\n")
print(short_response.content)


## Bullet Point Summary
bullet_prompt = PromptTemplate(
     input_variables=["text"],
    template="""
    You are an expert text summarizer.

    Summarize the following text in clear bullet points.
    Include the important concepts and key information.

    Text:
    {text}

    Bullet Point Summary:
    """
)

bullet_chain = bullet_prompt | model

bullet_response = bullet_chain.invoke({
    "text": text[:10000]
})


# Compare Outputs

print("\n========== SUMMARY COMPARISON ==========")

print("\n1. Short Summary:")
print(short_response.content)

print("\n2. Bullet Point Summary:")
print(bullet_response.content)



## Part 2 :Stuff Summarization Chain
## Task 4: Why Stuff Chain is needed

## Q.1: What is Stuff Summarization Chain ?
## Ans: A Stuff chain is a document summarization technique in LangChain that combines all input documents into a single prompt and sends that prompt to an LLM.

# In simple words:

# Stuff = Put all documents together + Send them to the LLM + Generate one summary.


## Q.2:  When is it Suitable to use?
## Ans: Stuff chain is suitable when:
# - The input document is relatively small.
# - All document content fits within the model's context window.
# - You want a single summary from multiple documents.
# - You want a simple summarization workflow with fewer LLM calls.

## Q.3: Limitation of Stuff Chain?
## Ans: 
# 1. Context Window Limitation: All documents must fit into the model's context window.
# 2. Large Document Problem: Very large PDFs may exceed the token limit.
# 3. Token Consumption: Sending all documents together can consume many tokens.
# 4. Cost: Larger prompts may increase API usage and cost.
# 5. Processing Limitation: It does not automatically summarize documents in smaller independent batches.


## Task 5:  Implement Stuff Summarization Chain

print("\n========== TASK 5: STUFF SUMMARIZATION ==========")

# Create Stuff Summarization Chain
stuff_chain = load_summarize_chain(
    model,
    chain_type="stuff"
)

# Select only the first few PDF pages
sample_documents = documents[:2]

# Pass the entire document
stuff_response = stuff_chain.invoke({
    "input_documents": sample_documents
})

print("\nStuff Chain Summary:\n")
print(stuff_response["output_text"])

# ==========================================
# Task 6: Comparison
# ==========================================

print("\n========== TASK 6: SUMMARY COMPARISON ==========")

print("\n1. Prompt-Based Summary:\n")
print(response.content)

print("\n2. Stuff Chain Summary:\n")
print(stuff_response["output_text"])


## Part 3:  Map-Reduce Summarization Chain
## Task 7: Why Map-Reduce is Needed 

## Q.1: Why large documents need map-reduce summarization ?
## Ans: Stuff Chain combines all documents into one prompt. When a document is very large, the combined prompt can exceed the model's available context or API limits.

# Map-Reduce solves this by dividing the document into smaller chunks and processing them separately.

## Q.2: How map and reduce steps works
## Ans: There are two main stages.

# MAP step
# - Takes individual chunks.
# - Sends each chunk to the LLM.
# - Generates a separate summary for each chunk.

# REDUCE step
# - Collects all individual summaries.
# - Combines them.
# - Sends the combined summaries to the LLM.
# - Generates one final summary.



# ==========================================
# Task 8: Map-Reduce Summarization Chain
# ==========================================

print("\n========== TASK 8: MAP-REDUCE SUMMARIZATION ==========")

# Create Map-Reduce Summarization Chain
map_reduce_chain = load_summarize_chain(
    model,
    chain_type="map_reduce",
    return_intermediate_steps=True,
    verbose=True
)
sample_chunks = chunks[:2]

# Pass all chunks to the chain
map_reduce_response = map_reduce_chain.invoke({
    "input_documents": sample_chunks
})

# Print individual chunk summaries
print("\nIndividual Chunk Summaries:\n")

for i, summary in enumerate(
    map_reduce_response["intermediate_steps"]
):
    print(f"\nChunk Summary {i+1}:")
    print(summary)

# Print final summary
print("\nFinal Map-Reduce Summary:\n")
print(map_reduce_response["output_text"])


## Part 4 : Refine Summarization Chain
## Task 10: Understanding Refine Chain

## Q.1: How refine Summary works?
## Ans: Refine is a document summarization technique in which the LLM generates an initial summary from the first chunk. It then processes subsequent chunks along with the existing summary and updates it with relevant information until all chunks are processed.

## Q.2:  Difference b/w map_reduce and refine
## Ans: Map-Reduce independently summarizes each chunk and then combines those summaries into a final summary. Refine generates an initial summary and progressively updates it using subsequent chunks. Map-Reduce supports parallel processing during the map stage, whereas Refine generally processes chunks sequentially.




# ==========================================
# Task 11: Refine Summarization Chain
# ==========================================

print("\n========== TASK 11: REFINE SUMMARIZATION ==========")

# Create Refine Summarization Chain
refine_chain = load_summarize_chain(
    model,
    chain_type="refine",
    return_intermediate_steps=True,
    verbose=True
)



# Pass all document chunks
refine_response = refine_chain.invoke({
    "input_documents": sample_chunks
})

# Print intermediate summaries
print("\nIntermediate Refined Summaries:\n")

for i, summary in enumerate(
    refine_response["intermediate_steps"]
):
    print(f"\nStep {i+1}:")
    print(summary)

# Print final refined summary
print("\nFinal Refined Summary:\n")
print(refine_response["output_text"])

# Task 14: Observations and Insights
## Q.1: Best summarization strategy for very long documents
## Ans: Map-Reduce is generally a suitable strategy for summarizing very long documents.

# Reasons:
# 1. It divides large documents into smaller chunks.
# 2. Each chunk is summarized independently during the Map stage.
# 3. The intermediate summaries are combined during the Reduce stage.
# 4. It can handle documents that are too large to fit into a single prompt.
# 5. The Map stage can process chunks in parallel in suitable implementations, improving processing speed.
# Refine is another useful strategy when we want to progressively update an existing summary using information from subsequent chunks.

# The best choice depends on document structure, context limits, processing time, and the level of detail required.


# Q.2: Trade-offs Between Speed and Quality
# - Prompt: Fast for short text, but limited by input size and prompt quality.
# - Stuff: Fast because it uses one main LLM call, but may exceed token limits for large documents.
# - Map-Reduce: Handles large documents effectively, but requires multiple LLM calls and may lose relationships between chunks.
# - Refine: Can produce a progressively updated summary, but is slower because chunks are processed sequentially.

# Q.3: Real-World Use Cases of Each Method
# Method	Real-world use cases
# Prompt	Summarizing emails, news articles, and short text.
# Stuff	Summarizing short PDF files, meeting notes, and small reports.
# Map-Reduce	Summarizing books, lengthy research papers, and large documents.
# Refine	Progressively updating research summaries, lengthy reports, and sequential document sections.
