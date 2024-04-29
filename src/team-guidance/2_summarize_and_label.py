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
ada2 = AzureOpenAIEmbeddings(azure_endpoint=os.environ['OPENAI_ENDPOINT'], 
                                    api_key=os.environ['OPENAI_API_KEY'],                                    
                                    model="ada-2", api_version="2023-05-15")

gpt = AzureChatOpenAI(azure_endpoint=os.environ['OPENAI_ENDPOINT'], 
                        api_key=os.environ['OPENAI_API_KEY'], 
                        deployment_name="gpt-35t", api_version="2023-05-15")

sys_prompt = SystemMessagePromptTemplate.from_template_file("_prompts/00_system.md", [])
summary_prompt = ChatMessagePromptTemplate.from_template_file("_prompts/01_summarize.md",
                                                    input_variables=['documentation'],
                                                    role="user")
summary_check_prompt = ChatMessagePromptTemplate.from_template_file("_prompts/01b_summary_check.md",
                                                    input_variables=['documentation'],
                                                    role="user")
tag_prompt = ChatMessagePromptTemplate.from_template_file("_prompts/02_classify.md",
                                                    input_variables=['documentation'],
                                                    role="user")   
tag_check_prompt = ChatMessagePromptTemplate.from_template_file("_prompts/02b_classify_check.md",
                                                    input_variables=['tags'],
                                                    role="user")       
                                                    
# Find markdown documentation files
repoFolders = cfg["folders"]
all_files = []
for repo in repoFolders:
    repoDir = "_data" + "/" + repo.replace("/", "_")
    folders = repoFolders[repo]

    files_in_folder = util.get_markdown_files(repoDir, folders)
    all_files = all_files + files_in_folder

progress = tqdm(range(len(all_files)))
for i in progress:
    entry = all_files[i]
    progress.write("Summarizing and labelling: " + entry['file'].name + "...")
    # Read the file contents
    with open(entry['file'], 'r') as f:
        content = f.read()

        # summarize the document
        sum_chain = (
            {"documentation": RunnablePassthrough()} 
            | ChatPromptTemplate.from_messages([sys_prompt, summary_prompt])
            | gpt 
            | {"summary": StrOutputParser() }
            | ChatPromptTemplate.from_messages([sys_prompt, summary_check_prompt])
            | gpt 
            | StrOutputParser()
        )

        # label/tag the document
        classify_chain = (
            {"documentation": RunnablePassthrough()} 
            | ChatPromptTemplate.from_messages([sys_prompt, tag_prompt]) 
            | gpt
            | {"tags": StrOutputParser()}
            | ChatPromptTemplate.from_messages([sys_prompt, tag_check_prompt]) 
            | gpt
            | StrOutputParser()
        )

        summary = sum_chain.invoke(content[:4000]) # Limiting to 4K for model token limits
        tags = classify_chain.invoke(content[:4000])

        result = {
            'title': entry['file'].name.replace(".md", "").replace("_", " "),            
            'content': summary, 
            'tags': tags,
            'contentVector': ada2.embed_documents([summary]),
            'titleVector': ada2.embed_documents([entry['file'].name]),
            'URL': 'https://learn.microsoft.com/en-us/azure/' + entry['folder'] + '/' + entry['file'].name.replace(".md", "")
        }
        
        # write this to a file
        fn = entry['file'].name.replace(".md", ".json")
        with open("_processed/" + fn, 'w') as f:
            f.write(json.dumps(result, indent=4))

logger.success("Summarized and classified " + str(len(all_files)) + " documents")