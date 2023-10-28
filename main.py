from fastapi import FastAPI
from multi_doc_chatbot import ask_chatbot, document_loader, tools

app = FastAPI()

@app.post("/ask")
def ask_endpoint(query: str= "Who is Juan Garcia?"):
    answer = ask_chatbot(query)
    return {'Answer': answer}

@app.get('/embed')
def get_context():
    docs = document_loader()
    tools.create_embeddings(docs, persist_directory='/root/langchain-chatbot/data')
    return {"status": "success", "message": "Embeddings created. "}
