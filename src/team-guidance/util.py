import github, git, os
from pathlib import Path
from loguru import logger

class util:
    @staticmethod
    def download_repo_to_folder(gh_repo, folder):      
        # Find clone URL
        gh = github.Github()
        url = gh.get_repo(gh_repo).clone_url        
        logger.info("GitHub repo URL: " + url)        
        
        # Clone if not already downloaded
        if not os.path.exists(folder):
            os.makedirs(folder)
            git.Repo.clone_from(url, folder, multi_options="--depth=1")
            logger.info("GitHub repo cloned into: " + folder)  
        else:
            logger.info("GitHub repository already found in: " + folder)  

    @staticmethod
    def get_markdown_files(repoDir, folders):
        files = []
        for folder in folders:
            logger.info("Looking for markdown files in folder:" + folder)  
            path = repoDir + "/" + folder
            mds = list(Path(path).rglob("*.md"))

            for md in mds:
                files.append({
                    "file": md,
                    "folder": folder.replace('articles/',"")
                })

            logger.info("Found " + str(len(mds)) + " markdown files")
        
        return files