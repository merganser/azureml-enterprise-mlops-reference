import argparse
import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

parser = argparse.ArgumentParser()
parser.add_argument("--subscription-id", required=True)
parser.add_argument("--resource-group", required=True)
parser.add_argument("--workspace", required=True)
parser.add_argument("--endpoint", required=True)
parser.add_argument("--output", default="test-attestation.json")
args = parser.parse_args()
client = MLClient(
    DefaultAzureCredential(), args.subscription_id, args.resource_group, args.workspace
)
request = {
    "input_data": [
        {
            "sepal length (cm)": 5.1,
            "sepal width (cm)": 3.5,
            "petal length (cm)": 1.4,
            "petal width (cm)": 0.2,
        }
    ]
}
with NamedTemporaryFile(mode="w", suffix=".json", encoding="utf-8", delete=False) as handle:
    json.dump(request, handle)
    request_path = handle.name
response = client.online_endpoints.invoke(
    endpoint_name=args.endpoint, request_file=request_path, deployment_name="blue"
)
parsed = json.loads(response)
if len(parsed.get("predictions", [])) != 1:
    raise SystemExit("Endpoint smoke test returned an invalid response")
attestation = {"endpoint": args.endpoint, "passed": True, "response": parsed}
Path(args.output).write_text(json.dumps(attestation, indent=2), encoding="utf-8")
