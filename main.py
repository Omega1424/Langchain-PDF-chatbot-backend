from fastapi import FastAPI
from multi_doc_chatbot import ask_chatbot

app = FastAPI()

@app.get("/ask")
def ask_endpoint(query: str= "Who is Juan Garcia?"):
    answer = ask_chatbot(query)
    return {'Answer': answer}