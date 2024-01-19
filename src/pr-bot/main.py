import os
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate,SystemMessagePromptTemplate, ChatPromptTemplate, PipelinePromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI

## Using OpenAI GPT-3 model deployed in Azure
model = AzureChatOpenAI(azure_endpoint="https://nl-stu-jvw-openai.openai.azure.com", 
                        api_key=os.environ['OPENAI_API_KEY'], 
                        deployment_name="gpt-3", api_version="2023-05-15")

## Force JSON repsonse
sys_prompt = SystemMessagePromptTemplate.from_template_file("templates/_system.txt", [])
usr_prompt = ChatMessagePromptTemplate.from_template_file("templates/01_question.txt", [], role="user")
prompt = ChatPromptTemplate.from_messages([sys_prompt, usr_prompt])

## Since sys prompt forces JSON response, we need to use a JSON output parser
## And look for 'data' property (see _system.txt template)
output_parser = JsonOutputParser()
def print_response(json): print(json['data'])

## Create a pipeline (chain) of prompts
chain = prompt \
            | model \
            | output_parser \
            | print_response

chain.invoke({})