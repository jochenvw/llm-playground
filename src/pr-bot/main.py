from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI
import openai

prompt = ChatPromptTemplate.from_template("Namaste - can you tell met the meaning of the word 'Namaste' in English?")
model = AzureChatOpenAI(azure_endpoint="https://nl-stu-jvw-openai.openai.azure.com", api_key="8d364dc5b892411991e25933af75863c", deployment_name="gpt-3", api_version="2023-05-15")
output_parser = StrOutputParser()

chain = prompt | model | output_parser | print

chain.invoke({})