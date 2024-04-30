# Log to KQL

Attempt to prove the ability of a Large Language Model (LLM) to write Kusto Query Language (KQL) against logfiles to automatically extract relevant information from the tsv/csv/...whatever log file format **WIP**

## Architecture Decision Records (ADRs)
Some ligtweight documentation of the decisions made in this project can be found in the [docs/](./docs/) folder.

- [Use Promptflow as orchestration library](./docs/adr_promptflow.md)
- [Use Semantic Kernel as LLM interaction library](./docs/adr_semantic_kernel.md)

# Get started

## Pre-reqs

- VSCode
- DevContainer extension installed (requires docker and perhaps WSL2)
- Azure subscription

## Setting up your environment

Ensure env variables are set. Lookg at `.env.example` for the required variables and copy to a `.env` file. Then run the following command to set the environment variables:

```
set -a # automatically export all variables
source .env
set +a
```

Check:
```
printenv | grep AZURE
```

