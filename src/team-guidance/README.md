# Large Language Models (LLMs) for Dev Team Guidance

This playground sets out to explore the use of Large Language Models (LLMs) for providing guidance to development teams. It aims to:

- Give guidance with the latest information on the cloud platform the teams lands on
- Taylors the 'generic' guidance to the specific context of the team (i.e. the org requirements to adoption of the cloud platform)
- Makes the guidance actionable and concrete

Future wish: incorporate this so that the guidance is as pro-active as possible, and 'shifted-left' as much as possible.

## Getting started

## 1. Start dev container
After cloning the repositry, run the [dev container](https://code.visualstudio.com/docs/devcontainers/containers).

## 2. Install python pre-reqs

```bash
cd .\src\team-guidance
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Deploy Azure resources

Ensure you have the Azure CLI installed in the dev container. If not - run `curl -L https://aka.ms/InstallAzureCli | bash`

Azure resources are within `.\src\_infra` folder:

1. Run `deploy.azcli` to deploy resource group and kick of the bicep template deployment (which is `main.bicep` and contains Azure OpenAI service + search service)
2. Back in `.\src\team-guidance`, copy `.env.example` to `.env` and fill in the values from the Azure resources deployed
3. Ensure env variables are loaded by running `source .env` - or run

    ```bash
    set -a # automatically export all variables
    source .env
    set +a
    ```
    Run `printenv | grep SEARCH` or `printenv | grep OPENAI` to ensure the values are loaded.
4. Run `python 0_create_index.py` to create the search index in the Azure Search service


## 4. Download the Azure Documentation

Repository size is approx 5GB or so - so this will take some time. 
We're doing 'shallow clone' to prevent the history from being downloaded (`git clone --depth=1` - [more info](https://github.blog/2020-12-21-get-up-to-speed-with-partial-clone-and-shallow-clone/))


```bash
python 1_download_azure_docs.py
```

## 5. Summarize and label
In order to subset the relevant Azure Docs - this step finds folders defined in `config.yaml` and summarizes the markdown files in them.

1. Gets the markdown files in the specified folders
2. Runs the prompts as can be found in `_prompts` folder. One for summarization, one for labelling - and embeds the content.
3. Writes the result as json into the `_processed` folder

```bash
python 2_summarize_and_label.py
```


## 6. Persist
Persist the summarized and labelled data into the Azure Search service

```bash
python 3_persist_to_search.py
```
