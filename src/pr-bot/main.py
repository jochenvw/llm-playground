import os, yaml, tempfile, github, git
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate,SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from pathlib import Path
from loguru import logger

from bot import Bot


## Using OpenAI GPT-3 model deployed in Azure
model = AzureChatOpenAI(azure_endpoint="https://nl-stu-jvw-openai.openai.azure.com", 
                        api_key=os.environ['OPENAI_API_KEY'], 
                        deployment_name="gpt4", api_version="2023-05-15")

cfgFilename = 'config.yaml'

## Get the GitHub repositories from config
with open(cfgFilename, 'r') as cfgFile:
    cfg = yaml.safe_load(cfgFile)

logger.success("Loaded config from: '" + cfgFilename + "' - OK!")
logger.success("Config contained " + str(len(cfg["repos"]["GitHub"])) + " GitHub repositories")
gh_repos = cfg["repos"]["GitHub"]

repos = Bot.CheckoutRepos(gh_repos, model)

for repo in repos:
    logger.info("📋 Working on GitHub repo: <green>" + repo["id"] + "</green>")

    for assessment in cfg["assessments"]:
        logger.trace("Running assessment " + assessment["name"] + " - on repository " + repo["id"])
        result = Bot.RunAssessment(assessment, repo["folder"], repo["iac_files"], model)
