
from flask import Flask, request, jsonify
from flask_cors import CORS
from inference_sdk import InferenceHTTPClient
import tempfile
import cv2

app = Flask(__name__)
CORS(app)

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="你的APIKEY"
)

MODEL_ID = "hand-gestures-detection-oqyzc/1"


@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return jsonify({"error": "没有文件"}), 400

    file = request.files["file"]

    temp = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp.name)

    cap = cv2.VideoCapture(temp.name)

    predictions = []

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_path = temp.name + ".jpg"

        cv2.imwrite(frame_path, frame)

        result = client.infer(frame_path, model_id=MODEL_ID)

        predictions.append(result)

    cap.release()

    return jsonify(predictions)


if __name__ == "__main__":
    app.run(port=5000)

