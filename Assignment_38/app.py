
import streamlit as st

from code_assistant import (
    generate_code,
    explain_code,
    fix_code,
    optimize_code,
    run_code_assistant
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Code Assistant",
    page_icon="💻",
    layout="wide"
)

st.title("💻 AI Code Assistant")
st.caption("Generate, understand, debug, and optimize your code using AI.")


# ==========================================
# SESSION STATE
# ==========================================

if "generated_code" not in st.session_state:
    st.session_state.generated_code = ""

if "code_input" not in st.session_state:
    st.session_state.code_input = ""


def load_generated_code():
    st.session_state.code_input = st.session_state.generated_code


# ==========================================
# FEATURE SELECTION
# ==========================================

task = st.selectbox(
    "Select a Feature",
    [
        "Code Generation",
        "Code Explanation",
        "Bug Fixing",
        "Code Optimization",
        "Full Code Assistant"
    ]
)

language = st.selectbox(
    "Programming Language",
    ["Python", "PHP", "JavaScript", "Java", "C++", "Other"]
)


# ==========================================
# 1. CODE GENERATION
# ==========================================

if task == "Code Generation":

    st.subheader("Generate Code")

    requirement = st.text_area(
        "Enter your coding requirement",
        placeholder="Create a function to find duplicate elements in a list."
    )

    if st.button("Generate Code", type="primary"):

        if requirement.strip():

            with st.spinner("Generating code..."):

                response = generate_code(
                    requirement=requirement,
                    language=language
                )

                st.session_state.generated_code = response
                st.session_state.code_input = response

            st.success("Code generated successfully!")

            st.subheader("Generated Code")
            st.code(response, language=language.lower())

        else:
            st.warning("Please enter your coding requirement.")


# ==========================================
# 2. FULL CODE ASSISTANT
# ==========================================

elif task == "Full Code Assistant":

    st.subheader("Complete Code Assistant")

    requirement = st.text_area(
        "Enter your coding requirement",
        placeholder="Create a function to find duplicate elements in a list."
    )

    if st.button("Run Complete Assistant", type="primary"):

        if requirement.strip():

            try:

                with st.spinner(
                    "Generating code and running analysis..."
                ):

                    result = run_code_assistant(
                        requirement=requirement,
                        language=language
                    )

                st.session_state.generated_code = result["generated_code"]
                st.session_state.code_input = result["generated_code"]

                st.success("Code Assistant completed!")

                # Generated Code
                st.subheader("1. Generated Code")

                st.code(
                    result["generated_code"],
                    language=language.lower()
                )

                # Code Explanation
                st.subheader("2. Code Explanation")
                st.markdown(result["analysis"]["explanation"])

                # Bug Fixing
                st.subheader("3. Bug Fixing")
                st.markdown(result["analysis"]["bug_fix"])

                # Code Optimization
                st.subheader("4. Code Optimization")
                st.markdown(result["analysis"]["optimization"])

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

        else:
            st.warning("Please enter your coding requirement.")


# ==========================================
# 3. COMMON CODE INPUT
# ==========================================

elif task in [
    "Code Explanation",
    "Bug Fixing",
    "Code Optimization"
]:

    st.subheader(task)

    if st.session_state.generated_code:

        st.button(
            "Load Previously Generated Code",
            on_click=load_generated_code
        )

    code = st.text_area(
        "Enter your source code",
        height=250,
        key="code_input",
        placeholder="Paste your code here..."
    )


    # ======================================
    # 3.1 CODE EXPLANATION
    # ======================================

    if task == "Code Explanation":

        if st.button("Explain Code", type="primary"):

            if code.strip():

                with st.spinner("Explaining code..."):

                    response = explain_code(
                        code=code,
                        language=language
                    )

                st.success("Explanation generated!")

                st.subheader("Code Explanation")
                st.markdown(response)

            else:
                st.warning("Please enter your source code.")


    # ======================================
    # 3.2 BUG FIXING
    # ======================================

    elif task == "Bug Fixing":

        error_description = st.text_area(
            "Enter error message or bug description",
            placeholder="Example: TypeError: unsupported operand type"
        )

        if st.button("Fix Bugs", type="primary"):

            if code.strip():

                with st.spinner("Analyzing and fixing bugs..."):

                    response = fix_code(
                        code=code,
                        language=language,
                        error_description=error_description
                    )

                st.success("Bug analysis completed!")

                st.subheader("Bug Fixing Result")
                st.markdown(response)

            else:
                st.warning("Please enter your source code.")


    # ======================================
    # 3.3 CODE OPTIMIZATION
    # ======================================

    elif task == "Code Optimization":

        if st.button("Optimize Code", type="primary"):

            if code.strip():

                with st.spinner("Analyzing code performance..."):

                    response = optimize_code(
                        code=code,
                        language=language
                    )

                st.success("Code analysis completed!")

                st.subheader("Optimization Suggestions")
                st.markdown(response)

            else:
                st.warning("Please enter your source code.")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption("Powered by LangChain + Ollama + CodeLlama 7B")
