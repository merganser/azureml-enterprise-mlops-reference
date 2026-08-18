FROM mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04:latest
WORKDIR /opt/mlops
COPY pyproject.toml ./
COPY src ./src
RUN python -m pip install --no-cache-dir .
USER 1000
