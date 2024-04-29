import os, yaml, json
from loguru import logger
from util import util

cfgFilename = 'config.yaml'

# Load config
with open(cfgFilename, 'r') as cfgFile:
    cfg = yaml.safe_load(cfgFile)

logger.success("Loaded config from: '" + cfgFilename + "' - OK!")
logger.success("Config contained " + str(len(cfg["repos"]["GitHub"])) + " GitHub repositories")
gh_repos = cfg["repos"]["GitHub"]


# Get (clone) the repositories with documentation
for repo in gh_repos:
    logger.info("📋 Working on GitHub repo: <green>" + repo + "</green>")

    repoDir = "_data" + "/" + repo.replace("/", "_")
    util.download_repo_to_folder(repo, repoDir)

