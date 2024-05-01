import asyncio
import semantic_kernel as sk
from dotenv import load_dotenv

import os

from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.planners import SequentialPlanner
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from promptflow.core import tool

from plugins.file_system import FileSystem



@tool
async def kql_generator_tool(input: str) -> str:
    # Ensures we read .env file variables
    load_dotenv()
    
    # Initialize the kernel
    kernel = sk.Kernel()
    kernel.add_service(AzureChatCompletion(
        service_id="azure_openai_text_completion",
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),            
        ))

    planner = SequentialPlanner(kernel=kernel, service_id="azure_openai_text_completion")
    kernel.add_plugin(FileSystem(), "FileSystem")

    ask = "Use the available filesystem functions to read the first lines of the following textfile: " + input
    
    plan =  await planner.create_plan(ask)

    # Execute the plan
    
    result = await plan.invoke(kernel=kernel)

    for index, step in enumerate(plan._steps):
        print("Function: " + step.plugin_name + "." + step._function.name)
        #print("Input vars: " + str(step.parameters))
        print("Output vars: " + str(step._outputs))
    print("Result: " + str(result))

    return str(result)
