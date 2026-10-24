## Task 3: Basic Message History
## Task 4: Trimming Chat History
## Task 5: Build Q&A Chatbot


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ('''system", "You are a helpful chatbot. Use the conversation history to answer naturally.
     Keep answer concise , around 100 words maximum,
     unless the user request more detail
     '''),
    MessagesPlaceholder(variable_name="history")
])

chain = prompt | llm

def trim_history(history):
    return trim_messages(
        history,
        max_tokens=500,
        token_counter="approximate",
        strategy="last",
        allow_partial=False,
        start_on="human"
    )

history = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    # Add the current user message
    history.append(HumanMessage(content=user_input))

    # print("HISTORY:" , history)

    history = trim_history(history)

    # Send the complete conversation history to the AI
    response = chain.invoke({"history": history})
    # print("DEBUG HISTORY:", history)

    print("AI:", response.content)

    # Save the AI response for the next turn
    history.append(AIMessage(content=response.content))
    print("History before trimming:", len(history))

    history = trim_history(history)
    print("History after trimming:", len(history))
    print("Token-limited history:", history)



