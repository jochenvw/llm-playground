import os, json
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from loguru import logger

key = os.environ["SEARCH_API_KEY"]
endpoint = os.environ["SEARCH_ENDPOINT"]

folder = '_processed/'

# list al files in folder
all_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

results = []
counter = 0
for f in all_files:
    # Upload some documents to the index
    with open(os.path.join(folder, f), 'r') as file:  
        doc = json.load(file)

    new_doc = {
        'id': doc['title'],
        'content': doc['content'],
        'tags': doc['tags'].split(','),
        'contentVector': doc['contentVector'][0],
        'titleVector': doc['titleVector'][0],
        'URL' : doc['URL']
    }
    results.append(new_doc)
    counter = counter + 1



search_client = SearchClient(endpoint=endpoint, index_name='azure_docs', credential=AzureKeyCredential(key))
result = search_client.upload_documents(results)

logger.success("Uploaded " + str(len(results)) + " documents to Azure Search index 'azure_docs'")

