from fastapi import FastAPI
from multi_doc_chatbot import ask_chatbot, document_loader, create_embeddings, tools

app = FastAPI()

@app.post("/ask")
def ask_endpoint(query: str= "Who is Juan Garcia?"):
    answer = ask_chatbot(query)
    return {'Answer': answer}

@app.get('/embed')
def get_context():
    if tools.qa_chain is None:
        docs = document_loader()
        create_embeddings(docs, persist_directory='/root/langchain-chatbot/data')
        return {"status": "success", "message": "Embeddings created and QA chain initialized."}
    else:
        return {"status": "info", "message": "Embeddings and QA chain are already initialized."}