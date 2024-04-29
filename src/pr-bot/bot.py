import os, yaml, tempfile, github, git, random
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate,SystemMessagePromptTemplate, ChatPromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from pathlib import Path
from loguru import logger

class Util:
    @staticmethod
    def extract_data(json):
        return json['data']


class Bot: 
    @staticmethod
    def RunAssessment(assessment, folder, files, model):        
        count = 0 + random.randrange(1000,9000)

        for file in files:
            logger.info("Running prompt " + assessment['name'] +" against file " + file + " .. ")

            # File filtering is not *perfect* :)
            path = folder + "/" + file
            if not os.path.exists(path):
                logger.warning("File " + path + " does not exist - skipping")
                continue
            if os.path.isdir(path):
                logger.warning("Path " + path + " is a directory - skipping")
                continue
            
            with open(path, "r") as f:
                oldCode = f.read()

            sys_prompt = SystemMessagePromptTemplate.from_template_file("_prompts/_system.md", [])
            check = ChatMessagePromptTemplate.from_template_file(assessment['explain-prompt'],
                                                                        input_variables=['input'],
                                                                        role="user")
            prompt_tpl = ChatPromptTemplate.from_messages([sys_prompt, check])

            assess = (
                {"input": RunnablePassthrough()} \
                | prompt_tpl \
                | model \
                | StrOutputParser() \
            )

            logger.info("Running prompt " + assessment['explain-prompt'] +" against file " + file + " .. ")            
            explanation = assess.invoke(oldCode)
            logger.info("LLM response: " + explanation)

            if explanation == "Looks OK - no changes needed :)":
                logger.success("No changes made to file " + file)
            else:               
                path = "output/" + assessment['name'] + "_" + str(count) + ".md"
                count += 1
                with open(path, "w") as f:
                    f.write(str(explanation))

                logger.success("Suggestions written to file " + path)


    @staticmethod
    def CheckoutRepos(repos, model):
        tmpDir = tempfile.TemporaryDirectory()
        response = []

        for id in repos:        
            logger.info("📋 Working on GitHub repo: " + id)
            gh = github.Github()
            url = gh.get_repo(id).clone_url        
            logger.info("GitHub repo URL: " + url)        
            
            repoDir = str(tmpDir) + "/" + id
            git.Repo.clone_from(url, repoDir)
            
            logger.info("GitHub repo cloned into: " + repoDir)

            files = list(Path(repoDir).rglob("*.*"))
            # join all the 'name' properties of the files into a comma-separated string
            filesStr = ", ".join([str(f) for f in files])
            filesStr = filesStr.replace(str(tmpDir), "")
            logger.info("GitHub repo contains " + str(len(files)) + " files")

            sys_prompt = SystemMessagePromptTemplate.from_template_file("_prompts/_system.md", [])
            get_iac = ChatMessagePromptTemplate.from_template_file("_prompts/01_id_iac_files.md",
                                                                        input_variables=['files'],
                                                                        role="user")
            prompt = ChatPromptTemplate.from_messages([sys_prompt, get_iac])

            ## Create a pipeline (chain) of prompts
            find_iac_files = (
                {"files": RunnablePassthrough()} \
                | prompt \
                | model \
                | JsonOutputParser() \
                | Util.extract_data
            )
            logger.info("Finding infra-as-code (IaC) file candidates in repository...")
            iac_files = find_iac_files.invoke(filesStr)

            # if more than one file found - log success, otherwise warning
            if len(iac_files) > 0:
                logger.success("LLM shortlisted following files: " + str(iac_files))
            else:
                logger.warning("LLM couldn't find any IaC files in repository: " + str(iac_files))

            response.append({
                "id": id,
                "clone_url": url,
                "folder": str(tmpDir),
                "iac_files": iac_files
            })

        return response

