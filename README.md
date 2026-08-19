# Azure ML Enterprise MLOps Reference

[![CI](https://github.com/merganser/azureml-enterprise-mlops-reference/actions/workflows/ci.yml/badge.svg)](https://github.com/merganser/azureml-enterprise-mlops-reference/actions/workflows/ci.yml)
[![CodeQL](https://github.com/merganser/azureml-enterprise-mlops-reference/actions/workflows/codeql.yml/badge.svg)](https://github.com/merganser/azureml-enterprise-mlops-reference/actions/workflows/codeql.yml)

An enterprise reference implementation for Azure Machine Learning with separate CI, Dev, Test, and Prod Azure DevOps pipelines, Snyk security gates, a shared Azure ML registry, managed online endpoints, and immutable asset promotion.

## Promotion model

1. **CI** validates code, runs Snyk SCA/SAST/container scans, builds the Python distribution and runtime image, registers versioned environments/components, and emits `promotion-manifest.json`.
2. **Dev** consumes the exact manifest versions, runs the training pipeline, applies the model-quality gate, and registers the qualified MLflow model in the shared registry.
3. **Test** deploys that exact model/runtime pair, invokes the endpoint, and emits `test-attestation.json`.
4. **Prod** requires the Test attestation and an Azure DevOps environment approval before deploying the same pair.

No downstream stage rebuilds application code or resolves `latest` asset aliases.

## Repository map

```text
aml/                 Azure ML environments, components, pipelines, endpoints
azure-pipelines/     Four pipeline definitions and reusable templates
config/              Environment-specific, non-secret configuration examples
docs/                Architecture and setup guidance
scripts/             Pipeline helpers, quality gate, and smoke test
src/                 Reusable Python package and scoring code
tests/               Unit tests
```

Start with [the architecture](docs/architecture.md) and then follow [the setup guide](docs/setup.md).

## GitHub validation

Every pull request and push to `main` runs Python linting, unit tests on Python 3.10–3.12, package build/install checks, YAML and rendered Azure ML template validation, and a production Docker image build. CodeQL and dependency review provide additional security checks. Azure-connected integration tests, Snyk gates, asset registration, and deployments remain in Azure DevOps because they require protected Azure service connections and environments.

## Important production choices

- Use workload identity federation for Azure service connections; avoid stored client secrets.
- Protect the shared registry and production resources with least-privilege RBAC and private networking where required.
- Enable ACR tag immutability or promote by image digest in regulated environments.
- Configure branch protection and require CI before merging to `main`.
- Store configuration in protected variable groups or Key Vault; no credentials belong in this repository.
