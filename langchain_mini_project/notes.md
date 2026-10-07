Important Components of Langchain

1) Model
2) Prompts
3) Chains
4) Memory
5) Indexes
6) Agents


1) Model: 

    1.1) LLM: Large Language Model: LLM (Large Language Model) is an AI model designed to understand and generate human language.
    Input: Mainly text
    Output: Mainly text
    Used for conversations, summarization, translation, coding, question answering, etc.

    1.2) Large Image Model: LIM (Large Image Model) generally refers to AI models designed to understand, analyze, or generate images.
    Input: Image and/or text, depending on the model
    Output: Image, image-related information, or text
    Used for image generation, image understanding, image analysis, etc.

    1.3) Multimodal Model: A multimodal model can work with multiple types of data (modalities) such as:
        Text
        Images
        Audio
        Video
        It can understand relationships between different types of inputs.

    1.4) Embedding Model: An embedding model converts data such as text, images, or other information into numerical vectors called embeddings.   

    These vectors represent the meaning or characteristics of the input in a form that computers can compare
    "King"
    ↓
    [0.21, -0.45, 0.73, 0.18, ...] 


Prompt Component of Langchain: 

1. Few-Shot Prompting: In Few-Shot Prompting, we provide a few examples of the expected input and output so the LLM can understand the desired pattern or format.

Input: I love this product.
Output: Positive

Input: This product is terrible.
Output: Negative

Input: The product is okay.
Output:

The model can infer that the expected answer is:
Neutral

Use: Helps the model follow a particular format, style, or pattern.

Chain of Thought Prompting: Chain-of-Thought (CoT) Prompting encourages a model to solve a problem through intermediate reasoning steps.

Example:

Question:
If I have 5 apples and buy 3 more, how many apples do I have?

Think through the problem step by step.

The model can reason:
5 + 3 = 8

Use: Useful for mathematical, logical, and multi-step problems.

Ask before Answer Prompting: This technique instructs the model to ask clarifying questions when the user's request is ambiguous or missing important information before generating the final answer.

User:
Book a hotel for me.

Model:
Which city would you like to stay in?
What dates do you need?
How many guests?

After receiving the required information, the model can provide an appropriate response.
Use: Helps reduce incorrect assumptions when important information is missing.

Fill-in-the-Blanks Prompting: In Fill-in-the-Blanks Prompting, part of the information is provided and the model is asked to complete the missing portion.

Python is a ______ programming language.
Possible output:
high-level

Use: Text completion, code completion, question answering, and structured data generation.

Reverse Prompting: Reverse Prompting means asking the model to create or improve the prompt itself based on the desired task or outcome.

Instead of directly giving the model a detailed prompt, you describe what you want and ask it to generate an effective prompt.

I want to generate a professional email
for requesting leave from my manager.

Create an effective prompt that I can give
to an LLM for this task.
The model generates a suitable prompt that can then be used with another LLM call.
Use: Prompt engineering, creating reusable prompts, and improving existing prompts.


RGC Prompting, (R means Role-Result, G means Goal, C means Context, constraint)
Role: ChatGPt Persons (Like you an expert marketer)
Result: Desired Output (create 5 emails ending with call to action)
Goal: Purpose of the Output (The goal is to drive sales to my product)
Context: Who, Where, What, Why [The Email are for my online entrepreneur]
Constraints: Limitation and Guidense (The email should be friendly and less than 100 words)



Prompt Formulas
1)  I want you to act as ("Bioliogist , Teacher", Interviwer) ---> ChatGpt Persona
2)  I will give you ------- a specific , Direction , product
3)  In a -------------- tone/style (Prefessional , tabular etc)
4)  The Important details are (Cost per Project )
5) Refine your prompt as needed



Chains in LangChain: Chains can helps us in building pipeline in our Ai Applications such that everything will be chain together.


Indexes in RAG (Retrieval-Augmented Generation) help an application organize and retrieve information from external knowledge sources such as PDFs, websites, databases, documents, etc.

Instead of giving all the external data directly to the LLM, the data is processed and indexed so that the relevant information can be retrieved when the user asks a question

PDF / Website / Database
          ↓
    Load the Data
          ↓
    Split into Chunks
          ↓
      Embeddings
          ↓
   Vector Index / Store
          ↓
      User Question
          ↓
   Retrieve Relevant Data
          ↓
        LLM
          ↓
     Final Answer

Suppose you have:
company_policy.pdf

The PDF contains 500 pages.
User asks: "What is the company's leave policy?"

RAG doesn't normally send all 500 pages to the LLM.
Instead:

Question
   ↓
Search the index
   ↓
Find relevant chunks about "leave policy"
   ↓
Send those chunks + question to LLM
   ↓
Generate answer

An index is not the external knowledge itself. It is a structure that makes the knowledge easier and faster to retrieve.
For modern RAG systems, a common approach is:
Documents → Chunks → Embeddings → Vector Store/Index → Retrieval → LLM

Memory and Agents: 
In LangChain, Memory helps an application maintain information from previous interactions so that the LLM can use the conversation context.

Conversation Buffer Memory: 


Agents:  For building AI-Agents we can use Agents Component of LangChain. 