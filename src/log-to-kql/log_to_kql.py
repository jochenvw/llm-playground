import asyncio
from promptflow.core import tool

import semantic_kernel as sk

from semantic_kernel.planners import SequentialPlanner
from plugins.FileSystem import FileSystem

from promptflow.connections import AzureOpenAIConnection
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureTextCompletion

@tool
def kql_generator_tool(
    input: str
) -> str:
    # Initialize the kernel
    kernel = sk.Kernel()
    
    kernel.add_text_completion_service(
        "text_completion",
        AzureTextCompletion(
            deployment_name,
            endpoint=os.getenv("OPENAI_ENDPOINT"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    )

    planner = SequentialPlanner(kernel=kernel)
    kernel.import_plugin(FileSystem(), "FileSystem")

    ask = "Use the available filesystem functions to read the following textfile: " + input

    plan = asyncio.run(planner.create_plan_async(ask))

    # Execute the plan
    result = asyncio.run(kernel.run_async(plan)).result

    for index, step in enumerate(plan._steps):
        print("Function: " + step.plugin_name + "." + step._function.name)
        print("Input vars: " + str(step.parameters.variables))
        print("Output vars: " + str(step._outputs))
    print("Result: " + str(result))

    return str(result)