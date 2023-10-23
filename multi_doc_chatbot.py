from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import sys
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader

openai_key = os.environ.get('OPENAI_API_KEY')
if openai_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

documents = []
for file in os.listdir('docs'):
    if file.endswith('.pdf'):
        pdf_path = '/root/langchain-chatbot/docs/' + file
        loader = PyPDFLoader(pdf_path)
        documents.extend(loader.load())
    elif file.endswith('.docx') or file.endswith('.doc'):
        doc_path = '/root/langchain-chatbot/docs/' + file
        loader = Docx2txtLoader(doc_path)
        documents.extend(loader.load())
    elif file.endswith('.txt'):
        text_path = '/root/langchain-chatbot/docs/' + file
        loader = TextLoader(text_path)
        documents.extend(loader.load())


# we split the data into chunks of 1,000 characters, with an overlap of 200 characters between the chunks, which helps to give better results and contain the context of the information between chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(documents)
vectordb = Chroma.from_documents(
  documents,
  embedding=OpenAIEmbeddings(),
  persist_directory='/root/langchain-chatbot/data'
)
vectordb.persist()

qa_chain = ConversationalRetrievalChain.from_llm(
    ChatOpenAI(model_name="gpt-3.5-turbo"),
    vectordb.as_retriever(search_kwargs={'k': 6}),
    return_source_documents=True
)
    
def ask_chatbot(query):
    if not query:
        return "please provide a question"
    result = qa_chain({'question':query, 'chat_history': []})
    answer = result.get('answer', "Sorry, I don't know")
    return answer