from langserve import add_routes
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel , Field
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from langchain_groq import ChatGroq
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

## Task 5: Create FastApi Application 

app = FastAPI()
client = Groq()

class ChatRequest(BaseModel):
    query:str
    

## Health Check Endpoint (# GET /health)
@app.get('/health')
def health_check():
    return {"status":"You are Healthy "}

## Chatbot endpoint (# POST /Chat)
@app.post('/chat')
def chat(request: ChatRequest):
    return {"answer": "Chatbot response will appear here"}



## Task 6: Fast Api + Groq Integraion

# def chat(request:ChatRequest):
    response = client.chat.completions.create(
        model = "openai/gpt-oss-120b",
        messages= [
            {
                "role":"system",
                "content": (
                            "You are a helpful assistant. "
                            "Give clear and simple answers. "
                            "The answer must not exceed 500 words. "
                            "Do not include unnecessary details."
                        )
            },
            {
                "role":"user",
                "content":request.query
            }
        ]
    )
    return {  "answer": response.choices[0].message.content}


