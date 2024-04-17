# Summary check

Check the summary below and ensure:
- Is written in valid markdown
- IF the document discusses a service deployment or configuration through the Azure Portal, you MUST insert a warning message as follows:
  "## **NOTE:** This document discusses configuration through the Azure Portal. Please _always_ use infrastructure-as-code (IaC) for production environments and deploy through Azure DevOps pipelines."
  This warning message must be inserted right under the title of the document.
- IF the document does not cover a service deployment or configuration through the Azure Portal, you MUST remove the warning message.
- If the summary is about any of the services that are prohibited from use within this organisation, you must NOT write a summary. You must then write "Service not allowed for use at the moment - please contact info@cloudteam.com for more information"
  Prohibited services are: Azure OpenAI service, Azure VMWare Service

Correct summary if necessary and resturn the updated summary in valid markdown.

# Begin summary
{summary}
# End summary