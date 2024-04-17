import os, yaml, json
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from loguru import logger

from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate,SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from tqdm import tqdm
from util import util


# Load config
cfgFilename = 'config.yaml'
with open(cfgFilename, 'r') as cfgFile:
    cfg = yaml.safe_load(cfgFile)


# Load the OpenAI models for embedding and chat
embeddings_model = AzureOpenAIEmbeddings(azure_endpoint=os.environ['OPENAI_ENDPOINT'], 
                                    api_key=os.environ['OPENAI_API_KEY'],                                    
                                    model="ada-2", api_version="2023-05-15")

model = AzureChatOpenAI(azure_endpoint=os.environ['OPENAI_ENDPOINT'], 
                        api_key=os.environ['OPENAI_API_KEY'], 
                        deployment_name="gpt-35t", api_version="2023-05-15")


# Find markdown documentation files
repoFolders = cfg["folders"]
all_files = []
for repo in repoFolders:
    repoDir = "_data" + "/" + repo.replace("/", "_")
    folders = repoFolders[repo]

    files_in_folder = util.get_markdown_files(repoDir, folders)
    all_files = all_files + files_in_folder

counter = 0
progress = tqdm(range(len(all_files)))
for i in progress:
    file = all_files[i]
    progress.write("Summarizing and labelling: " + file.name + "...")
    # Read the file contents
    with open(file, 'r') as f:
        content = f.read()

        prompt_system = SystemMessagePromptTemplate.from_template_file("_prompts/00_system.md", [])
        prompt_summary = ChatMessagePromptTemplate.from_template_file("_prompts/01_summarize.md",
                                                            input_variables=['documentation'],
                                                            role="user")
        prompt_classify = ChatMessagePromptTemplate.from_template_file("_prompts/02_classify.md",
                                                            input_variables=['documentation'],
                                                            role="user")        

        # Summarization
        sum_chain = (
            {"documentation": RunnablePassthrough()} 
            | ChatPromptTemplate.from_messages([prompt_system, prompt_summary])
            | model 
            | StrOutputParser() 
        )

        # Classification
        classify_chain = (
            {"documentation": RunnablePassthrough()} 
            | ChatPromptTemplate.from_messages([prompt_system, prompt_classify]) 
            | model
            | StrOutputParser()
        )

        result = {
            'summary': sum_chain.invoke(content[:4000]), # Limiting to 4K for model token limits
            'tags': classify_chain.invoke(content[:4000]),
            'embedding': embeddings_model.embed_documents(['content'])
        }
        
        # write this to a file
        with open("_processed/" + str(counter) + ".json", 'w') as f:
            f.write(json.dumps(result, indent=4))
            counter = counter + 1        

logger.success("Summarized and classified " + str(len(all_files)) + " documents")