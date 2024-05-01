# Even though stated - I can't find IO plugins for Semantic Kernel anywhere:
# - Stated here: https://learn.microsoft.com/en-us/semantic-kernel/agents/plugins/out-of-the-box-plugins?tabs=python#core-plugins 
# - Offical location: https://github.com/microsoft/semantic-kernel/tree/main/python/semantic_kernel/core_plugins 

from typing_extensions import Annotated
from semantic_kernel.functions.kernel_function_decorator import kernel_function

class FileSystem:
    @kernel_function(
        description="Reads the first lines of a file",
        name="ReadFileHead",
    )
    def ReadFileHead(
        self, 
        filename: Annotated[str, "The filename of the file to read"] 
    ) -> Annotated[str, "The output is a string containing the first lines of the file"]:
        with open(filename, "r") as f:
            result = ""
            for i in range(10):
                result += f.readline()
                
        return result