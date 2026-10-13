from langserve import add_routes
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv



load_dotenv()

class TranslationRequest(BaseModel):
    lang:str
    text:str
    


app = FastAPI()

@app.get('/hello')
def hello():
    return {"message":"HEllo , how are you "}

@app.post('/llm')
def translate(request:TranslationRequest):
    llm = ChatGroq(model="openai/gpt-oss-120b",temperature=0)
    prompt = PromptTemplate(template='Convert this {text} to from english to {lang}', input_variables=['text','lang'])
    parser = StrOutputParser()
    chain = prompt | llm | parser
    result = chain.invoke({'text':request.text, 'lang':request.lang })
    return {'translation':result}

