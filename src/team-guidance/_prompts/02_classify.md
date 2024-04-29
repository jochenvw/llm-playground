# Documentation classification prompt

Classify the following documentation into single words or "tags". 

The tags should represent:

- The service or technology the documentation is about.
- Azure Services must be prefixed by `azure-` (e.g. `azure-application-gateway`)
- The type of documentation (e.g. installation, configuration, troubleshooting)
- The sub-topic of the document. What component of the service or technology is the document about?

Ensure you follow these rules:

- You MUST return not more than 5 words/tags
- You MUST return a list of words as comma-separated values.
- You MUST return at least 1 word/tag
- You MUST make sure tags are lowercase
- Tags can be multi-word but then should have "-" and no spaces
- Tags MUST only contain letters and hyphens.
- Tags MUST NOT contain any special characters (like newline) or numbers.

Example of good tags:

- azure-application-gateway, ssl-policy, configuration
- azure-application-gateway, diagnostics, monitoring
- azure-application-gateway, scaling, availability, sys-ops

## Begin documentation

{documentation}

## End documentation