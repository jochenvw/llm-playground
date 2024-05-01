# Log to KQL

Attempt to prove the ability of a Large Language Model (LLM) to write Kusto Query Language (KQL) against logfiles to automatically extract relevant information from the tsv/csv/...whatever log file format **WIP**

## Architecture Decision Records (ADRs)
Some ligtweight documentation of the decisions made in this project can be found in the [docs/](./docs/) folder.

- [Use Promptflow as orchestration library](./docs/adr_promptflow.md)
- [Use Semantic Kernel as LLM interaction library](./docs/adr_semantic_kernel.md)

More on [ADRs](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records) | [Even more](https://adr.github.io/) | [Template used](https://adr.github.io/madr/#example)

# Get started

## Note on usage of virtual environments (VENVs)

Whereas I'm a proponent of using these - the VSCode plugins for Semantic Kernel and Prompflow seem to index these `.venv` in their totality. This makes it (at least on my machine) impossible to work with.
Therefore - I'm **not** using vritual environments for now.

`pip install -r requirements.txt` to get your depenedencies.

## Pre-reqs - tools

- VSCode
- DevContainer extension installed (requires docker and perhaps WSL2)
- Azure subscription
- Azure CLI: `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`

## Pre-reqs - environment

- Ensure env variables are set. Lookg at `.env.example` for the required variables and copy to a `.env` file. `dotenv` will take care of loading.
- Have Azure Monitor workspace deployed
- Have service principal that has access to the Azure Monitor workspace for testing KQL queries

