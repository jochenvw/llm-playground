# PR-Bot

Plan is to showcase the following:
- A Bot that pulls sources from a GitHub repostitory
- Runs a prompt to identity infra-as-code (IaC) files (e.g. Terraform, CloudFormation, etc.)
- Checks adherence to e.g. security practices, FinOps practices or any other prompt you can come up with
- Modify the code (not done yet)
- Create pull request to simplify adoption by the team that owns the code (not done yet)


## Findings
- Initially I set out to get the IaC files myself (globbing over some extensions) - then I decided to use a prompt.
  Turns out the prompt also included some files that I had overlooked (`.azcli` for instance)

## How to run
- Rename `.env.template` to .env
- Fill in the values in `.env` with your own values
- Load env variables `export $(xargs <.env)`
- Run using `python3 main.py`