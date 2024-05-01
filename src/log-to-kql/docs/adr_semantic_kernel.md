# Use Semantic Kernel as LLM interaction library

## Context and Problem Statement

An interesting feature of applications that leverage Generative AI (genAI), specifically Large Language Models (LLMs) to 'get stuff done', is the ability to leverage the LLMs 'planning' capabilities. This is where the LLM can be used to plan a sequence of actions to achieve a goal - as opposed to writing code to achieve the goal. 
GenAI applications that leverage LLMs to plan are often referred to as 'agents'.

Most libraries that aim to facilitate building genAI applictions, such as PromptFlow, LangChain, Graphlit, LlamaIndex, etc. have some form of 'planning' capability. 

Although perhaps over-engineering for this project, it is interesting to leverage the 'planning' capabilities of the LLMs to see how it can be used to plan the extraction of relevant information from log files.

Therefore selecting a library with 'planning' capabilities is required.

## Considered Options

- [Semantic Kernel](https://github.com/microsoft/semantic-kernel)

- [LangChain](https://github.com/langchain-ai/langchain)

## Decision Outcome

For this project, Semantic Kernel has been opted for. 

Arguments for this decision are:

- Plays nice with PromptFlow - see [./adr_promptlfow.md](./adr_promptlfow.md).
  See: https://learn.microsoft.com/en-us/semantic-kernel/agents/planners/evaluate-and-deploy-planners/

    > With Semantic Kernel you can build autonomous AI applications with the aid of plugins and planners. Creating autonomous AI applications, however, can be challenging because you need to ensure your plugins and planners consistently produce the desired results across a wide range of inputs. This is where Prompt flow can help.

- LangChain is used in some of the other experiments in this library - let's try something new.
- Some critical observations from ThoughtWorks Tech Radar: https://www.thoughtworks.com/radar/languages-and-frameworks/langchain 

    > We mentioned some of the emerging criticisms about LangChain in the previous Radar. Since then, we’ve become even more wary of it. While the framework offers a powerful set of features for building applications with large language models (LLMs), we’ve found it to be hard to use and overcomplicated. LangChain gained early popularity and attention in the space, which turned it into a default for many developers. However, as LangChain is trying to evolve and keep up with the fast pace of change, it has become harder and harder to navigate those changes of concepts and patterns as a developer. We’ve also found the API design to be inconsistent and verbose. As such, it often obscures what is actually going on under the hood, making it hard for developers to understand and control how LLMs and the various patterns around them actually work. We’re moving LangChain to the Hold ring to reflect this. 