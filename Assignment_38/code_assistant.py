from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Initialize LLM
llm = ChatOllama(
    model="codellama:7b",
    temperature=0
)


# Code Generation Prompt
code_generation_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert programming assistant.

    Generate clean, readable, and efficient code
    based on the user's requirements.

    Programming Language: {language}

    Requirement: {requirement}

    Provide only the generated code.
    """
)

# Create LCEL chain
code_generation_chain = (
    code_generation_prompt
    | llm
    | StrOutputParser()
)

# Code Generation Function
def generate_code(requirement, language):

    response = code_generation_chain.invoke({
        "requirement": requirement,
        "language": language
    })

    return response


result = generate_code(
    requirement="Create a function to find duplicate elements in a list.",
    language="Python"
)

print(result)
