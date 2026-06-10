from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# load .env  file
load_dotenv()


llm = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")
res = llm.invoke("Who is GENAI founder")
data = res.content
print(data)
