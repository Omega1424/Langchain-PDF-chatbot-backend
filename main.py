from fastapi import FastAPI
from multi_doc_chatbot import ask_chatbot, document_loader, create_embeddings

app = FastAPI()

@app.post("/ask")
def ask_endpoint(query: str= "Who is Juan Garcia?"):
    answer = ask_chatbot(query)
    return {'Answer': answer}
@app.get('/embed')
def get_context():
    docs = document_loader()
    return create_embeddings(docs)
