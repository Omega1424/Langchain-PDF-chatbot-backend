from platform import python_version
import os   
from langchain.document_loaders import PyPDFLoader
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

# we are specifying that OpenAI is the LLM that we want to use in our chain

os.environ["OPENAI_API_KEY"] = "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"

pdf_loader = PyPDFLoader('/root/langchain-chatbot/docs/RachelGreenCV.pdf')
documents = pdf_loader.load()
openai_llm = OpenAI(model_name="gpt-3.5-turbo")
chain = load_qa_chain(llm=openai_llm,verbose=True)
query = 'Give me a summary of the CV'
response = chain.run(input_documents=documents, question=query)
print(response) 
# if __name__ == "__main__":
#     print('lola')
#     documents