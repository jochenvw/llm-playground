import os, yaml, tempfile, github, git
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate,SystemMessagePromptTemplate, ChatPromptTemplate, PipelinePromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_core.runnables import RunnablePassthrough

from pathlib import Path


## Using OpenAI GPT-3 model deployed in Azure
model = AzureChatOpenAI(azure_endpoint="https://nl-stu-jvw-openai.openai.azure.com", 
                        api_key=os.environ['OPENAI_API_KEY'], 
                        deployment_name="gpt-3", api_version="2023-05-15")

with open('config.yaml', 'r') as cfgFile, tempfile.TemporaryDirectory() as tmpDir:
    cfg = yaml.safe_load(cfgFile)

    print(cfg["repos"]["GitHub"])

    for repo in cfg["repos"]["GitHub"]:
        print("Working on repo: " + repo + " ...")
        g = github.Github()
        url = g.get_repo(repo).clone_url
        
        repoDir = tmpDir + "/" + repo
        repo = git.Repo.clone_from(url, repoDir)
        print("Repository cloned to: " + repoDir)

        fs = list(Path(repoDir).rglob("*.*"))
        # join all the 'name' properties of the files into a comma-separated string
        f2 = ", ".join([f.name for f in fs])

        sys_prompt = SystemMessagePromptTemplate.from_template_file("_prompts/_system.txt", [])
        get_iac = ChatMessagePromptTemplate.from_template_file("_prompts/01_id_iac_files.txt",
                                                                     input_variables=['files'],
                                                                     role="user")
        prompt = ChatPromptTemplate.from_messages([sys_prompt, get_iac])

        ## Since sys prompt forces JSON response, we need to use a JSON output parser
        ## And look for 'data' property (see _system.txt template)
        def print_response(json): 
            print(json['data'])
            return json['data']

        ## Create a pipeline (chain) of prompts
        chain = (
            {"files": RunnablePassthrough()} \
            | prompt \
            | model \
            | JsonOutputParser() \
            | print_response
        )
        
        s = chain.invoke(f2)

        print("Done.")
