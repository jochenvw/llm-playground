# PR-Bot

Plan is to showcase the following:
- A Bot that pulls sources from a GitHub repostitory
- Runs a prompt to identity infra-as-code (IaC) files (e.g. Terraform, CloudFormation, etc.)
- Checks adherence to e.g. security practices, FinOps practices or any other prompt you can come up with
- Modify the code (not done yet)
- Create pull request to simplify adoption by the team that owns the code (not done yet)


## Example

Output:

<blockquote>

  ## Improvement
  
  1. All resources in a development environment should be tagged with a `CostCenter` tag with the value `Dev`. Currently the resources have no tags.
  
  2. All Azure platform services in a development environment should be Development SKU whenever possible. The function app plan currently uses the `ElasticPremium` tier which is not necessary for a development environment.
  
  ## Rationale
  
  1. Tagging with `CostCenter` allows for better tracking of costs associated with development resources. This is important for the organization to keep track of their expenses and to manage their cloud costs better.
  
  2. Using a Development SKU instead of `ElasticPremium` can save costs as the development environment doesn't need the extra capabilities provided by the `ElasticPremium` tier.
  
  ## Code suggestion
  
  Here are the changes that I would suggest:
  
  ```bicep
  
  resource functionstore 'Microsoft.Storage/storageAccounts@2021-02-01' = {
      name: functionAppStoreName
    location: defaultResourceLocation
    tags: {
        'CostCenter': 'Dev'
    }
    ....
  }
  
  ...
  
  resource functionappplan 'Microsoft.Web/serverfarms@2020-12-01' = {
      name: functionAppPlanName
    location: defaultResourceLocation
    kind: 'elastic'
    tags: {
        'CostCenter': 'Dev'
    }
    sku: {
        'name': 'F1'
      'tier': 'Free'
      'capacity': 1
    }
  }
  
  ...
  
  // Repeat this tag addition for all resources
  
  ```
  
  This code adds a `CostCenter` tag with the value `Dev` to all resources and changes the SKU of the function app plan to `F1` which is the free tier."
</blockquote>


## Findings
- Initially I set out to get the IaC files myself (globbing over some extensions) - then I decided to use a prompt.
  Turns out the prompt also included some files that I had overlooked (`.azcli` for instance)

## How to run
- Rename `.env.template` to .env
- Fill in the values in `.env` with your own values
- Load env variables `export $(xargs <.env)`
- Run using `python3 main.py`