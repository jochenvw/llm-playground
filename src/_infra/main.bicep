param loc string = 'swedencentral'

resource openai_svc 'Microsoft.CognitiveServices/accounts@2023-10-01-preview' = {
  name: 'nl-stu-jvw-openai'
  location: loc
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {}
}

resource store 'Microsoft.Search/searchServices@2024-03-01-preview' = {
  name: 'nl-stu-jvw-search'
  location: loc
  sku: {
    name: 'standard'
  }
  properties: {}
}
