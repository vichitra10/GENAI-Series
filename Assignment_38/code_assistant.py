
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough
)


# ==========================================
# Initialize LLM
# ==========================================

llm = ChatOllama(
    model="codellama:7b",
    temperature=0,
    num_predict=1024,
    repeat_penalty=1.1,
    num_ctx=2048
)

parser = StrOutputParser()


# ==========================================
# 1. CODE GENERATION
# ==========================================

code_generation_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert programming assistant.

    Generate clean, readable, and efficient code
    based on the user's requirements.

    Programming Language: {language}

    Requirement: {requirement}

    Provide only the generated code.
    Do not include explanations.
    """
)

code_generation_chain = (
    code_generation_prompt
    | llm
    | parser
)


def generate_code(requirement, language):

    response = code_generation_chain.invoke({
        "requirement": requirement,
        "language": language
    })

    return response


# ==========================================
# 2. CODE EXPLANATION
# ==========================================

code_explanation_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert programming instructor.

    Explain the given code in a clear and understandable way.

    Programming Language: {language}

    Code:
    {code}

    Explain:
    1. Purpose of the code.
    2. Step-by-step working.
    3. Important functions and logic.
    4. Expected output (if applicable).

    Make the explanation beginner-friendly.
    """
)

code_explanation_chain = (
    code_explanation_prompt
    | llm
    | parser
)


def explain_code(code, language):

    response = code_explanation_chain.invoke({
        "code": code,
        "language": language
    })

    return response


# ==========================================
# 3. BUG FIXING
# ==========================================

bug_fixing_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert software developer and debugging specialist.

    Analyze the given code and identify the bugs.

    Programming Language: {language}

    Code:
    {code}

    Error Message or Bug Description:
    {error_description}

    Perform the following tasks:

    1. Identify the problem.
    2. Explain why the problem occurs.
    3. Provide the corrected code.
    4. Explain what changes you made.

    If the code is already correct, mention that.
    Do not invent errors.
    """
)

bug_fixing_chain = (
    bug_fixing_prompt
    | llm
    | parser
)


def fix_code(code, language, error_description):

    response = bug_fixing_chain.invoke({
        "code": code,
        "language": language,
        "error_description": error_description
    })

    return response


# ==========================================
# 4. CODE OPTIMIZATION SUGGESTIONS
# ==========================================

code_optimization_prompt = ChatPromptTemplate.from_template(
    """
    You are an expert software engineer specializing in
    code optimization and performance improvement.

    Analyze the given code and suggest possible optimizations.

    Programming Language: {language}

    Code:
    {code}

    Focus on the following:

    1. Time complexity.
    2. Space complexity.
    3. Performance improvements.
    4. Code readability and maintainability.
    5. Best programming practices.

    Provide:
    - Current code analysis.
    - Potential performance bottlenecks.
    - Specific optimization suggestions.
    - Optimized code example, if improvements are possible.

    Do not suggest unnecessary changes.
    Explain why each optimization is useful.
    """
)

code_optimization_chain = (
    code_optimization_prompt
    | llm
    | parser
)


def optimize_code(code, language):

    response = code_optimization_chain.invoke({
        "code": code,
        "language": language
    })

    return response


# ==========================================
# MAIN EXECUTION
# ==========================================

# if __name__ == "__main__":

#     requirement = "Create a function to find duplicate elements in a list."

#     language = "Python"

#     # 1. Generate Code
#     generated_code = generate_code(requirement, language)

#     print("\n========== GENERATED CODE ==========")
#     print(generated_code)

#     # 2. Explain Generated Code
#     explanation = explain_code(generated_code, language)

#     print("\n========== CODE EXPLANATION ==========")
#     print(explanation)

#     # 3. Fix Bugs in Generated Code
#     fixed_code = fix_code(
#         code=generated_code,
#         language=language,
#         error_description="Check for logical errors and potential bugs."
#     )

#     print("\n========== BUG FIXING ==========")
#     print(fixed_code)

#     # 4. Suggest Code Optimizations
#     optimization = optimize_code(generated_code, language)

#     print("\n========== CODE OPTIMIZATION ==========")
#     print(optimization)


# ==========================================
# 5. COMBINED CODE ASSISTANT WORKFLOW
# ==========================================

# Run all three analysis chains in parallel
code_analysis_chain = RunnableParallel(
    explanation=code_explanation_chain,
    bug_fix=bug_fixing_chain,
    optimization=code_optimization_chain
)


# Generate code first, then analyze it
code_assistant_chain = (
    RunnablePassthrough.assign(
        generated_code=code_generation_chain
    )

    | RunnablePassthrough.assign(
        code=lambda x: x["generated_code"]
    )

    | RunnablePassthrough.assign(
        analysis=code_analysis_chain
    )
)


# ==========================================
# 6. COMBINED WORKFLOW FUNCTION
# ==========================================

def run_code_assistant(requirement, language):

    response = code_assistant_chain.invoke(
        {
        "requirement": requirement,
        "language": language,
        "error_description": "Check the code for logical errors and potential bugs."
        },
        config={"max_concurrency": 1}
    )

    return response