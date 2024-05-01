from typing_extensions import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from dotenv import load_dotenv
from datetime import timedelta

import os

from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

class AzureMonitor:
    @kernel_function(
        description="Executes a KQL against an Azure Monitor workspace",
        name="ExecuteKQL",
    )
    def ReadFileHead(
        self, 
        kql_query: Annotated[str, "The KQL query to execute"] 
    ) -> Annotated[str, "The result of the KQL query"]:        
        load_dotenv()
        
        credential = DefaultAzureCredential()
        logs_query_client = LogsQueryClient(credential)
        
        # Bit of hack - ask Stef how to avoid this
        kql_query = kql_query.replace("[END KQL]", "")
        
        try:
            result = logs_query_client.query_workspace(os.getenv("WORKSPACE_ID"), kql_query, timespan=timedelta(hours=1))
            return kql_query
        except Exception as e:
            print(kql_query)
            print(e)
            return "ERROR"