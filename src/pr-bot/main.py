import os, yaml, tempfile, github, git
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate,SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from pathlib import Path
from loguru import logger


## Using OpenAI GPT-3 model deployed in Azure
model = AzureChatOpenAI(azure_endpoint="https://nl-stu-jvw-openai.openai.azure.com", 
                        api_key=os.environ['OPENAI_API_KEY'], 
                        deployment_name="gpt-3", api_version="2023-05-15")

cfgFilename = 'config.yaml'
with open(cfgFilename, 'r') as cfgFile, tempfile.TemporaryDirectory() as tmpDir:
    cfg = yaml.safe_load(cfgFile)
    logger.success("Loaded config from: '" + cfgFilename + "' - OK!")
    logger.success("Config contained " + str(len(cfg["repos"]["GitHub"])) + " GitHub repositories")

    for repo in cfg["repos"]["GitHub"]:        
        logger.info("📋 Working on GitHub repo: " + repo)
        gh = github.Github()
        url = gh.get_repo(repo).clone_url        
        logger.info("GitHub repo URL: " + url)        
        
        repoDir = tmpDir + "/" + repo
        repo = git.Repo.clone_from(url, repoDir)
        logger.info("GitHub repo cloned into: " + repoDir)

        files = list(Path(repoDir).rglob("*.*"))
        # join all the 'name' properties of the files into a comma-separated string
        filesStr = ", ".join([f.name for f in files])
        logger.info("GitHub repo contains " + str(len(files)) + " files")

        sys_prompt = SystemMessagePromptTemplate.from_template_file("_prompts/_system.txt", [])
        get_iac = ChatMessagePromptTemplate.from_template_file("_prompts/01_id_iac_files.txt",
                                                                     input_variables=['files'],
                                                                     role="user")
        prompt = ChatPromptTemplate.from_messages([sys_prompt, get_iac])

        ## Since sys prompt forces JSON response, we need to use a JSON output parser
        ## And look for 'data' property (see _system.txt template)
        def print_response(json): 
            # print(json['data'])
            return json['data']

        ## Create a pipeline (chain) of prompts
        find_iac_files = (
            {"files": RunnablePassthrough()} \
            | prompt \
            | model \
            | JsonOutputParser() \
            | print_response
        )
        logger.info("Finding infra-as-code (IaC) file candidates in repository...")
        iac_files = find_iac_files.invoke(filesStr)

        # if more than one file found - log success, otherwise warning
        if len(iac_files) > 0:
            logger.success("LLM shortlisted following files: " + str(iac_files))
        else:
            logger.warning("LLM couldn't find any IaC files in repository: " + str(iac_files))



        # sec = ChatMessagePromptTemplate.from_template_file("_prompts/02_sec_assess.txt",
        #                                                              input_variables=['code'],
        #                                                              role="user")
        # prompt = ChatPromptTemplate.from_messages([sys_prompt, sec])

        # sec_assess = (
        #     {"code": RunnablePassthrough()} \
        #     | prompt \
        #     | model \
        #     | JsonOutputParser() \
        #     | print_response
        # )
        # logger.info("Doing security assessment of infra-as-code (IaC) files...")
        # s = sec_assess.invoke(f2)
                        
