# Use Promptflow as orchestration library

## Context and Problem Statement

A typical application interacting with a Large Language Model (LLM) often contains a series of steps (workflow) to be executed in a specific order. The steps may be dependent on each other, and the order of execution is important. The orchestration of these steps could warrant the use of an orchestration library.

The library should be able to handle the following:

- Workflow management (visual would be nice): inter-dependent steps, outputs as inputs etc.
- Facilitate testing and debugging
- Different modes to run: debug, test (batch?)
- Facilitate 'productionalizing' - i.e. wrap in container and expose endpoint

## Considered Options

* [PromptFlow](https://github.com/microsoft/promptflow) 
    > Prompt flow is a suite of development tools designed to streamline the end-to-end development cycle of LLM-based AI applications, from ideation, prototyping, testing, evaluation to production deployment and monitoring. It makes prompt engineering much easier and enables you to build LLM apps with production quality.

* [LangChain](https://github.com/langchain-ai)
    > LangChain is a framework for developing applications powered by large language models (LLMs).

* [Graphlit](https://www.graphlit.com/)
  >If you are familiar with open source projects like LangChain or LlamaIndex, those libraries are a great 'bag of tools' when building your own Knowledge Applications.
  > But what they aren't is a cloud-native service, which provides secure content storage, recurrent data feeds, automated data workflows, data modelling, entity resolution, multi-tenant support and usage-based tracking and billing.
  > Graphlit is API-first - we manage a serverless cloud-native data platform for your applications to build on.

* [LlamaIndex](https://docs.llamaindex.ai/en/stable/)
    > LlamaIndex is a framework for building context-augmented LLM applications. Context augmentation refers to any use case that applies LLMs on top of your private or domain-specific data. Some popular use cases include the following:
    > 
    > Question-Answering Chatbots (commonly referred to as RAG systems, which stands for "Retrieval-Augmented Generation")
    > Document Understanding and Extraction
    > Autonomous Agents that can perform research and take actions
    > LlamaIndex provides the tools to build any of these above use cases from prototype to production. The tools allow you to both ingest/process this data and implement complex query workflows combining data access with LLM prompting.


Links found in this thread:
https://learn.microsoft.com/en-us/semantic-kernel/agents/planners/evaluate-and-deploy-planners/


## Decision Outcome
To be fair - not extensive research has been done on the different options. However - for this project, for now, PromptFlow has been opted for.

Features in favor of PromptFlow:
- VSCode integration: https://marketplace.visualstudio.com/items?itemName=prompt-flow.prompt-flow
- Testing is built-in: https://microsoft.github.io/promptflow/how-to-guides/develop-a-dag-flow/init-and-test-a-flow.html
- Productionalize quickly to Docker Container: https://microsoft.github.io/promptflow/how-to-guides/deploy-a-flow/deploy-using-docker.html
- Has batch capabilities that parallelizes over threads, which is useful for the many documents that need to be processed in parallel.