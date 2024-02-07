import os, yaml, tempfile, github, git
from langchain_core.output_parsers import JsonOutputParser
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
    def RunAssessment(prompt, files, model):
        for file in files:
            logger.info("Running prompt " + prompt +" against file " + file + " .. ")

            with open(file, "r") as f:
                oldCode = f.read()

            sys_prompt = SystemMessagePromptTemplate.from_template_file("_prompts/_system.txt", [])
            get_iac = ChatMessagePromptTemplate.from_template_file(prompt,
                                                                        input_variables=['input'],
                                                                        role="user")
            prompt = ChatPromptTemplate.from_messages([sys_prompt, get_iac])

            assess = (
                {"input": RunnablePassthrough()} \
                | prompt \
                | model \
                | JsonOutputParser() \
                | Util.extract_data
            )

            logger.info("Running prompt " + prompt +" against file " + file + " .. ")
            newCode = assess.invoke(oldCode)

            if newCode == oldCode:
                logger.success("No changes made to file " + file)
            else:               
                # overwrite the contents of file f with newcode
                with open(file, "w") as f:
                    f.write(newCode)

                logger.success("Changes made to file " + file)


    @staticmethod
    def CheckoutRepos(repos, model):
        tmpDir = tempfile.TemporaryDirectory()
        response = []

        for id in repos:        
            logger.info("📋 Working on GitHub repo: " + id)
            gh = github.Github()
            url = gh.get_repo(id).clone_url        
            logger.info("GitHub repo URL: " + url)        
            
            repoDir = tmpDir + "/" + id
            git.Repo.clone_from(url, repoDir)
            
            logger.info("GitHub repo cloned into: " + repoDir)

            files = list(Path(repoDir).rglob("*.*"))
            # join all the 'name' properties of the files into a comma-separated string
            filesStr = ", ".join([str(f) for f in files])
            logger.info("GitHub repo contains " + str(len(files)) + " files")

            sys_prompt = SystemMessagePromptTemplate.from_template_file("_prompts/_system.txt", [])
            get_iac = ChatMessagePromptTemplate.from_template_file("_prompts/01_id_iac_files.txt",
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
                "folder": repoDir,
                "iac_files": iac_files
            })

        return response

