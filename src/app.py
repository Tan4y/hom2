from flask import Flask, request, jsonify
import boto3
import jwt
from config import MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET

app = Flask(__name__)

# Настройка на MinIO клиента
s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    s3_client.upload_fileobj(file, MINIO_BUCKET, file.filename)
    return jsonify({"message": f"File {file.filename} uploaded successfully!"}), 200

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    try:
        file_obj = s3_client.get_object(Bucket=MINIO_BUCKET, Key=file_id)
        return file_obj['Body'].read(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/update/<file_id>', methods=['PUT'])
def update_file(file_id):
    file = request.files['file']
    s3_client.upload_fileobj(file, MINIO_BUCKET, file_id)
    return jsonify({"message": f"File {file_id} updated successfully!"}), 200

@app.route('/delete/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    try:
        s3_client.delete_object(Bucket=MINIO_BUCKET, Key=file_id)
        return jsonify({"message": f"File {file_id} deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
