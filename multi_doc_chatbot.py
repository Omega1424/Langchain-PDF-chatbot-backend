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

class ChatbotTools:
    _instance = None  # Singleton instance
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatbotTools, cls).__new__(cls)
            cls._instance.vectordb = None
            cls._instance.qa_chain = None
        return cls._instance
    
    def __init__(self):
        self.vectordb = None
        self.qa_chain = None
    
    def create_vectordb(self, documents, persist_directory):
        self.vectordb = Chroma.from_documents(
            documents,
            embedding=OpenAIEmbeddings(),
            persist_directory=persist_directory
        )
        self.vectordb.persist()
        
    def create_qa_chain(self):
        if self.vectordb is None:
            raise ValueError("vectordb needs to be created first!")
        
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(model_name="gpt-3.5-turbo"),
            self.vectordb.as_retriever(search_kwargs={'k': 3}),
            return_source_documents=True
        )


tools = ChatbotTools()  

def document_loader():
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
    return documents

# we split the data into chunks of 1,000 characters, with an overlap of 200 characters between the chunks, which helps to give better results and contain the context of the information between chunks
persist_directory = '/root/langchain-chatbot/data'

def create_embeddings(documents, persist_directory):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    chunked_documents = text_splitter.split_documents(documents)
    tools.create_vectordb(documents, persist_directory)  # Using chunked_documents
    tools.create_qa_chain()

chat_history = []

def ask_chatbot(query):
    if not query:
        return "please provide a question"
    prompt = query + "Answer the question based on only the context given. If you don't know the answer say I don't know"
    
    if tools.qa_chain is None:
        raise ValueError("The qa_chain hasn't been initialized!")
    
    result = tools.qa_chain({'question': prompt, 'chat_history': chat_history})
    answer = result.get('answer', "Sorry, I don't know")
    chat_history.append({
        'query': query,
        'answer': answer
    })
    if len(chat_history) > 4:
        chat_history.pop(0)
    return answer