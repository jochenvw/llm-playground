# Documentation summarization prompt

Summarize the following documentation in 2500 words.

Ensure to adhere to the following:
- Keep your summary concise and to the point - do not include any fluff
- You must summarize and use language that is understandable by an IT Pro
- Do NOT recomend anything to be done manually or through the Azure Portal
- IF the document discusses a service deployment or configuration through the Azure Portal, you MUST insert a warning message as follows:
  "## **NOTE:** This document discusses configuration through the Azure Portal. Please _always_ use infrastructure-as-code (IaC) for production environments and deploy through Azure DevOps pipelines."
  This warning message must be inserted right under the title of the document.

- You must make sure to include sample and code snippets relevant for automation
- You must respond in valid markdown

# Begin documentation
{documentation}
# End documentation