# PDF-Chatbot Backend

## About 
API for chatbot using Langchain and GPT3.5-turbo model that can take in multiple documents and answer relevant questions. Backend was built using FastAPI.
## Set up Locally
1. Clone repo `git clone https://github.com/Omega1424/Langchain-PDF-chatbot`
2. Add your documents to the `docs` directory
3. Login to [OpenAI]
(https://platform.openai.com/account/api-keys) and obtain API key. Go to cmd prompt and set up environment variable with `setx OPENAI_API_KEY “<yourkey>”`
4. Create Docker image `docker-compose build`
5. Create and start container instance and run application `docker-compose up`