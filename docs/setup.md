# Setup

## Azure resources

Provision an Azure ML registry, three workspaces, an Azure Container Registry, and a CPU cluster in each workspace. Grant each pipeline identity only the permissions required for its environment. The CI identity needs push access to ACR and asset-create access to the Azure ML registry.

## Azure DevOps service connections

Create these service connections and secret variables in a protected variable group:

- `azureServiceConnection`, `azureServiceConnectionDev`, `azureServiceConnectionTest`, `azureServiceConnectionProd`
- `acrServiceConnection`, `acrLoginServer`, `amlRegistry`, `subscriptionId`
- `devResourceGroup`, `devWorkspace`, `devCompute`
- `testResourceGroup`, `testWorkspace`, `testEndpoint`
- `prodResourceGroup`, `prodWorkspace`, `prodEndpoint`

Install the Snyk Security Scan extension and create the `snyk` service connection. Create four pipeline definitions pointing to `azure-pipelines/ci.yml`, `dev.yml`, `test.yml`, and `prod.yml`, named `AzureML-CI`, `AzureML-DEV`, `AzureML-TEST`, and `AzureML-PROD`.

Add an approval/check to the `azureml-prod` Azure DevOps environment. Restrict the production service connection and variable group to the Prod pipeline.

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
ruff check .
pytest
```
