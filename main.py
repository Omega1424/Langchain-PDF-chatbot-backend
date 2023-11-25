
import logging
from fastapi import FastAPI
from multi_doc_chatbot import ask_chatbot, document_loader, tools
from pydantic import BaseModel
import os


logging.basicConfig(
    level=logging.DEBUG,     # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
app = FastAPI()

class Item(BaseModel):
    query: str
    
@app.post("/ask")
def ask_endpoint(item: Item):
    query = item.query
    answer = ask_chatbot(query)
    logging.info(query)
    return {'Answer': answer}
    
@app.get('/embed')
def get_context():
    docs = document_loader()
    persist_directory=os.path.expanduser('~/langchain-chatbot/data')
    tools.create_embeddings(docs, persist_directory=persist_directory)
    return {"status": "success", "message": "Embeddings created. "}