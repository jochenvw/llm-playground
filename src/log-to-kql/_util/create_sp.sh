#!/usr/bin/env bash

SCRIPT_NAME='create-azure-service-principal-contrib.sh'
SCRIPT_DESCRIPTION='Creates an Azure AD service principal with Contributor rights'
SCRIPT_VERSION='1.2.2'

# Related documentation:
# - https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli

function display_usage() {
# echo "------------------------------------------------------------------------"
  echo ""
  echo "Usage: $SCRIPT_NAME [<SERVICE_PRINCIPAL_NAME>|--help|--license]"
  echo ""
  echo "Creates an Azure AD service principal in the current subscription with"
  echo "default assignment (Contributor) in the default scope (Subscription)."
  echo ""
  echo "Optional arguments"
  echo "  -h  --help      Display usage information (this text)."
  echo "  -v  --version   Display version and license information."
  echo ""
  echo "Executing the Script"
  echo ""
  echo "This script is intended to be run interactively, and is best run from"
  echo "Azure Cloud Shell, as Cloud Shell already supports the commands"
  echo "required.  If you already have Azure CLI and jq on your PATH, it will"
  echo "work just fine in other contexts."
  echo ""
  echo "Example:"
  echo "    $SCRIPT_NAME sp-deploy-contrib-sub"
  echo ""
  echo "Setting the Subscription"
  echo ""
  echo "Make certain the correct subscription is set prior to running the script."
  echo "If you need to change the subscription, you can do so with the following"
  echo "command:"
  echo ""
  echo " az account set -s SUBSCRIPTION_NAME_OR_ID"
  echo ""
  echo "See 'az account set -h' for more information."
  echo ""
  exit $1
}

function display_version() {
  echo "$SCRIPT_NAME $SCRIPT_VERSION"
  echo ""
  echo "Copyright (c) 2019-2021 Craig Forrester"
  echo ""
  echo "MIT License: <https://mit-license.org/>"
  echo ""
  echo "Permission is hereby granted, free of charge, to any person"
  echo "obtaining a copy of this software and associated documentation files"
  echo '(the "Software"), to deal in the Software without restriction,'
  echo "including without limitation the rights to use, copy, modify, merge,"
  echo "publish, distribute, sublicense, and/or sell copies of the Software,"
  echo "and to permit persons to whom the Software is furnished to do so,"
  echo "subject to the following conditions:"
  echo ""
  echo "The above copyright notice and this permission notice shall be included"
  echo "in all copies or substantial portions of the Software."
  echo ""
  echo 'THE SOFTWARE IS PROVIDED "AS ISr, WITHOUT WARRANTY OF'
  echo "ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE"
  echo "WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND"
  echo "NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE"
  echo "LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION"
  echo "OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION"
  echo "WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."
  echo ""
  exit $1
}

NORMAL="\e[0m"
BOLD="\e[1m"
BLUE="\e[94m"
CYAN="\e[96m"
GRAY="\e[90m"
GREEN="\e[92m"
RED="\e[91m"
YELLOW="\e[93m"

function verify_subscription() {
  echo ""
# az account set -s "$SUBSCRIPTION_ID"

  az account list \
    --query "[?isDefault].{SubscriptionName:name,SubscriptionID:id,IsDefault:isDefault}" \
    --output table |
    GREP_COLORS='ms=01;32' \
    grep -E --color=always '.*True|$'

  echo -e "\n${YELLOW}Proceed using the subscription shown?${NORMAL}\n"
  read -p "Enter to continue or Ctrl-C to cancel: " RESPONSE
}


if [ ! -x "$(which jq)" ] ; then
  echo -e '\e[91mERROR: This script requires the jq command to be installed in the PATH.\e[39m'
  exit 3
fi

if [[ "$1"x == 'x' ]]; then
  echo -e '\e[91mERROR: No Service Principal name supplied.\e[39m'
  display_usage 2
elif [[ "$1" == '-h' ]] || [[ "$1" == '--help' ]]; then
  display_usage 0
elif [[ "$1" == '-v' ]] || [[ "$1" == '--version' ]]; then
  display_version 0
else
  SERVICE_PRINCIPAL_NAME="$1"
fi

verify_subscription

AZURE_ACCOUNT_JSON=$(az account list --query "[?isDefault]" -o json)

SERVICE_PRINCIPAL_SUBSCRIPTION_NAME=$(echo $AZURE_ACCOUNT_JSON | jq -r .[].name)
SERVICE_PRINCIPAL_SUBSCRIPTION_ID=$(echo $AZURE_ACCOUNT_JSON | jq -r .[].id)
SERVICE_PRINCIPAL_TENANT_ID=$(echo $AZURE_ACCOUNT_JSON | jq -r .[].tenantId)

SERVICE_PRINCIPAL_SECRET=$(az ad sp create-for-rbac \
                            --name "$SERVICE_PRINCIPAL_NAME" \
                            --scope "/subscriptions/$SERVICE_PRINCIPAL_SUBSCRIPTION_ID" \
                            --role 'Contributor' \
                            --query password \
                            --output tsv)

SERVICE_PRINCIPAL_JSON=$(az ad sp list --filter "displayname eq '$SERVICE_PRINCIPAL_NAME' and servicePrincipalType eq 'Application'"  --output json)

SERVICE_PRINCIPAL_TENANT_NAME=$(echo $SERVICE_PRINCIPAL_JSON | jq -r .[].publisherName)
SERVICE_PRINCIPAL_APP_ID=$(echo $SERVICE_PRINCIPAL_JSON | jq -r .[].appId)
SERVICE_PRINCIPAL_OBJECT_ID=$(echo $SERVICE_PRINCIPAL_JSON | jq -r .[].objectId)
SERVICE_PRINCIPAL_NAMES=$(echo $SERVICE_PRINCIPAL_JSON | jq -r '.[].servicePrincipalNames | @tsv')

echo -e "\nAzure Service Principal Information:"
echo "***************************************************************************"
echo "Subscription Id: ${SERVICE_PRINCIPAL_SUBSCRIPTION_ID}"
echo "Subscription Name: ${SERVICE_PRINCIPAL_SUBSCRIPTION_NAME}"
echo "Object ID: ${SERVICE_PRINCIPAL_OBJECT_ID}"
echo "Service Principal Client (Application) Id: ${SERVICE_PRINCIPAL_APP_ID}"
echo "Service Principal Key: ${SERVICE_PRINCIPAL_SECRET}"
echo "Tenant Id: ${SERVICE_PRINCIPAL_TENANT_ID}"
echo "Service Principal Display Name: ${SERVICE_PRINCIPAL_NAME}"
echo "Service Principal Names:"
for NAME in $SERVICE_PRINCIPAL_NAMES; do
  echo "   *  ${NAME}"
done
echo "***************************************************************************"
echo -e "Credentials File (.azure/credentials)"
echo "# ${SERVICE_PRINCIPAL_TENANT_NAME}: ${SERVICE_PRINCIPAL_SUBSCRIPTION_NAME} (${SERVICE_PRINCIPAL_SUBSCRIPTION_ID})"
echo "[default]"
echo "client_id=${SERVICE_PRINCIPAL_APP_ID}"
echo "secret=${SERVICE_PRINCIPAL_SECRET}"
echo "subscription_id=${SERVICE_PRINCIPAL_SUBSCRIPTION_ID}"
echo "tenant=${SERVICE_PRINCIPAL_TENANT_ID}"
echo "***************************************************************************"
echo -e "Environment Variables for HashiCorp Terraform:"
echo "export ARM_CLIENT_ID=${SERVICE_PRINCIPAL_APP_ID}"
echo "export ARM_CLIENT_SECRET=${SERVICE_PRINCIPAL_SECRET}"
echo "export ARM_SUBSCRIPTION_ID=${SERVICE_PRINCIPAL_SUBSCRIPTION_ID}"
echo "export ARM_TENANT_ID=${SERVICE_PRINCIPAL_TENANT_ID}"
echo "***************************************************************************"
echo -e "Environment Variables:"
echo "export AZURE_CLIENT_ID=${SERVICE_PRINCIPAL_APP_ID}"
echo "export AZURE_SECRET=${SERVICE_PRINCIPAL_SECRET}"
echo "export AZURE_SUBSCRIPTION_ID=${SERVICE_PRINCIPAL_SUBSCRIPTION_ID}"
echo "export AZURE_TENANT=${SERVICE_PRINCIPAL_TENANT_ID}"
echo "***************************************************************************"

# EOF