# PDF-Chatbot Backend
![Architectural Diagram](/architecture%20diagram.png)
## About 
API for chatbot using Langchain and GPT3.5-turbo model that can take in multiple documents and answer relevant questions. Backend was built using FastAPI.
## Set up Locally
1. Clone repo `git clone https://github.com/Omega1424/Langchain-PDF-chatbot`
2. Add your documents to the `docs` directory
3. Login to [OpenAI]
(https://platform.openai.com/account/api-keys) and obtain API key. Go to cmd prompt and set up environment variable with `setx OPENAI_API_KEY “<yourkey>”`
4. Create Docker image `docker-compose build`
5. Create and start container instance and run application `docker-compose up`
## Deploy web-app
1. Repeat step 1 to 3 for local set up
2. Build docker image locally
    - `docker build -t <image name> .`
3. Create Resource Group on Azure (or use existing one)
4. Create Container Registry (ACR)
    - Basics
        - Choose Resource Group
        - Location: South East Asia
5. Login
    - `az login`
    - `az acr login --name <acr name>`
6. Tag image locally
    - `docker tag <image name> <your-acr-name>.azurecr.io/<image name>:<tag>`
7. Push image to ACR
    - `docker push <your-acr-name>.azurecr.io/<image name>:<tag>`
8. Create App Service on Azure
    - Web app
        - Basics
            - Publish: Docker container
            - Runtime Stack: Depending on your python version
            - Region: Southeast Asia
        - Docker:
            - Options: Single Container
            - Image Source: Azure Container Registry
            - Choose registry, image and tag
        
9. Get URL 
    - App Service → Overview → Default Domain
      
Optional:
10. Change docker image that App Service uses
    - App Service → Deployment Center → Choose registry, image and tag
11. Once everything in the app works properly, change to CI/CD (Continuous Integration/Deployment)
    - App Service → Deployment Center
        - GitHub Actions → Continuous Deployment:enable
        - Preview file, copy file contents into local directory of `<project dir>/.github/workflow` and name it `<name>.yml`
        - Push to GitHub
