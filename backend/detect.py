from inference_sdk import InferenceHTTPClient

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="SGTJcfHAUNXpxqQzdrMR"
)

MODEL_ID = "hand-gestures-detection-oqyzc/1"

def detect(image_path):
    result = client.infer(image_path, model_id=MODEL_ID)
    return result