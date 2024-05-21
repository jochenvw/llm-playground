import os, yaml
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate,SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

## Using OpenAI GPT-3 model deployed in Azure
model = AzureChatOpenAI(azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
                        api_key=os.environ['AZURE_OPENAI_API_KEY'], 
                        deployment_name=os.environ['AZURE_OPENAI_DEPLOYMENT_NAME'], api_version="2023-05-15")

cfgFilename = 'config.yaml'

## Get the GitHub repositories from config
with open(cfgFilename, 'r') as cfgFile:
    cfg = yaml.safe_load(cfgFile)

logger.success("Loaded config from: '" + cfgFilename + "' - OK!")

for item in cfg['process_queue']:
    logger.success("Working on file " + item['in'] + "...")
    
    with open(item['in'], 'r') as f:
        csv = f.read()

    sys_prompt = SystemMessagePromptTemplate.from_template_file("_prompts/_system.md", [])
    transform_tpl = ChatMessagePromptTemplate.from_template_file(item['prompt'],
                                                                input_variables=['input'],
                                                                role="user")
    prompt_tpl = ChatPromptTemplate.from_messages([sys_prompt, transform_tpl])

    chain = (
        {"input": RunnablePassthrough()} \
        | prompt_tpl \
        | model \
        | StrOutputParser() \
    )
    
    logger.trace("Transforming data ...")
    response = chain.invoke(csv)
    logger.trace("Transformation done!")
    
    with open(item['out'], 'w') as file:
        file.write(response)
        logger.success("Wrote to file " + item['out'] + " - OK!")


    logger.success("Done!")
