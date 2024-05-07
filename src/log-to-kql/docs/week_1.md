# 'Sprint 1' recap: 'Hello KQL'
Here's where we're at today (May 7th). We've been building an application that reads a sample apache logfile and uses an LLM (GPT hosted in Azure OpenAI service) to generate KQL.

## What's been done

- [x] Set up 'walking skeleton' of the the application written in Python, using [PromptFlow](./adr_promptflow.md) and [Semantic Kernel](./adr_semantic_kernel.md). Click to find out _why_ we've opted for these libraries.
- [x] Instantiate a planner that is responsible for the task/goal execution ([../goal.txt](../goal.txt)):
  - Read log file
  - Use GPT to create a KQL query that detects and extracts the fields.
  - Use GPT to filter these columns to only the ones that are relevant.
  - Return the KQL query


    ```mermaid
    sequenceDiagram
        Promptflow->>Semantic Kernel:start
        Semantic Kernel->>GPT:CreatePlan
        GPT->>Semantic Kernel: 


        Semantic Kernel->>Plugins:ReadFile
        Plugins->>Semantic Kernel: 

        Semantic Kernel->>GPT:Extract Fields KQL
        GPT->>Semantic Kernel: 

        Semantic Kernel->>Plugins:CheckKQL
        Plugins->>Azure Monitor:ExecuteKQL
        Azure Monitor->>Plugins: 
        Plugins->>Semantic Kernel: 

        Semantic Kernel->>GPT:Filter Columns
        GPT->>Semantic Kernel: 
        
        Semantic Kernel->>GPT:Filter Output
        GPT->>Semantic Kernel: 
        
        Semantic Kernel->>GPT:Convert to JSON
        GPT->>Semantic Kernel: 

        Semantic Kernel->>Plugins:WriteFile
        Plugins->>Semantic Kernel: 
    ```


## What's been learnt

- Modifying and tweaking prompts is complicated and time consuming. And still GPT does not always 'do what you want'.
Interesing post on-topic: [Musings on building a Generative AI product](https://www.linkedin.com/blog/engineering/generative-ai/musings-on-building-a-generative-ai-product)

- Semantic Kernel _also_ suffers from inconsistencies in documentation (so similar to the critique that LangChain gets). Semantic Kernel is available in Python, .NET and JAVA which can be confusing when looking for sample code. Also, a lot of the sample code is outdated and does not work against the latest version of the library.

- GPT model version very significantly impacts performance. E.g. GPT 3.5 turbo vs GPT 4 is a huge difference. Both in terms of performance but also in terms of response quality predictability.

## What's next

- [ ] Operationalisation of the application - how to 'get it in production'? How do we get this to Azure and where do we run it?
- [ ] Lightweight well-architected review of the design, consider operational excellence (e.g. logging), security of course etc.
- [ ] Consider using 'handlebars' plans that allow for loops: [https://devblogs.microsoft.com/semantic-kernel/migrating-from-the-sequential-and-stepwise-planners-to-the-new-handlebars-and-stepwise-planner/](https://devblogs.microsoft.com/semantic-kernel/migrating-from-the-sequential-and-stepwise-planners-to-the-new-handlebars-and-stepwise-planner/)

