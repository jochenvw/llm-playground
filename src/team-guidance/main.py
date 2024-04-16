import git.repo
import os, yaml, tempfile, github, git
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate,SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from pathlib import Path
from loguru import logger

from langchain_openai import OpenAIEmbeddings

embeddings_model = AzureOpenAIEmbeddings(azure_endpoint="https://swedencentral.api.cognitive.microsoft.com/", 
                                    api_key=os.environ['OPENAI_API_KEY'],                                    
                                    model="ada-2", api_version="2023-05-15")

## Using OpenAI GPT-3 model deployed in Azure
model = AzureChatOpenAI(azure_endpoint="https://swedencentral.api.cognitive.microsoft.com/", 
                        api_key=os.environ['OPENAI_API_KEY'], 
                        deployment_name="gpt4", api_version="2023-05-15")

cfgFilename = 'config.yaml'

## Get the GitHub repositories from config
with open(cfgFilename, 'r') as cfgFile:
    cfg = yaml.safe_load(cfgFile)

logger.success("Loaded config from: '" + cfgFilename + "' - OK!")
logger.success("Config contained " + str(len(cfg["repos"]["GitHub"])) + " GitHub repositories")
gh_repos = cfg["repos"]["GitHub"]


# Get (clone) the repositories
for repo in gh_repos:
    logger.info("📋 Working on GitHub repo: <green>" + repo + "</green>")

    repoDir = "_data" + "/" + repo.replace("/", "_")

    # Find clone URL
    gh = github.Github()
    url = gh.get_repo(repo).clone_url        
    logger.info("GitHub repo URL: " + url)        
    
    # Clone if not already downloaded
    if not os.path.exists(repoDir):
        os.makedirs(repoDir)
        git.Repo.clone_from(url, repoDir, multi_options="--depth=1")
        logger.info("GitHub repo cloned into: " + repoDir)  
    else:
        logger.info("GitHub repository already found in: " + repoDir)  


# Find the relevat files
repoFolders = cfg["folders"]
for repo in repoFolders:
    repoDir = "_data" + "/" + repo.replace("/", "_")

    folders = repoFolders[repo]
    for folder in folders:
        path = repoDir + "/" + folder
        files = list(Path(path).rglob("*.md"))
        for file in files:
            logger.info("📄 Found MarkDown file: <green>" + str(file) + "</green>")
            with open(file, 'r') as f:
                content = f.read()
                embeddings_model.embed_documents([content])


# Tokens per Minute Rate Limit (thousands): 120
# Rate limit (Tokens per minute): 120000
# Rate limit (Requests per minute): 720
