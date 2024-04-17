# Documentation summarization prompt

Summarize the following documentation in 2500 words.

Your response should adhere to the following:
- Keep your summary concise and to the point - do not include any fluff
- You must summarize and use language that is understandable by an IT Pro
- You must make sure to include sample and code snippets relevant for automation
- You must respond in valid markdown


The response context should consider the following:
- Do NOT recomend anything to be done manually or through the Azure Portal
- IF the document discusses a service deployment or configuration through the Azure Portal, you MUST insert a warning message as follows:
  "## **NOTE:** This document discusses configuration through the Azure Portal. Please _always_ use infrastructure-as-code (IaC) for production environments and deploy through Azure DevOps pipelines."
  This warning message must be inserted right under the title of the document.
- If the document discusses any of the services that are prohibited from use within this organisation, you must NOT write a summary. You must then write "Service not allowed for use at the moment - please contact info@cloudteam.com for more information"
  Prohibited services are: Azure OpenAI service, Azure VMWare Service


# Begin documentation
{documentation}
# End documentation