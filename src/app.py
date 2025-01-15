from flask import Flask, request, jsonify
import boto3
import jwt
from config import MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET
from config import KEYCLOAK_URL, KEYCLOAK_CLIENT_ID, KEYCLOAK_CLIENT_SECRET, KEYCLOAK_PUBLIC_KEY

app = Flask(__name__)

# Настройка на MinIO клиента
s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1"
)

# JWT Authentication function (Keycloak)
def validate_jwt(token):
    try:
        # Decode JWT and verify with Keycloak's public key
        decoded_token = jwt.decode(token, KEYCLOAK_PUBLIC_KEY, algorithms=["RS256"], audience=KEYCLOAK_CLIENT_ID)
        return decoded_token
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/')
def index():
    return 'Welcome to the File Management API! Visit /upload to upload a file, /download/<file_id> to download a file, /update/<file_id> to update a file, and /delete/<file_id> to delete a file.'

@app.route('/upload', methods=['POST'])
def upload_file():
    # Extract Authorization header (JWT token)
    token = request.headers.get("Authorization")
    if not token:
        app.logger.info("Missing authorization token")
        return jsonify({"error": "Missing authorization token"}), 401
    token = token.split(" ")[1]  # Assuming Bearer token format

    # Validate the token
    decoded_token = validate_jwt(token)
    if not decoded_token:
        app.logger.info("Invalid or expired token")
        return jsonify({"error": "Invalid or expired token"}), 401

    # Log file upload attempt
    file = request.files.get('file')
    if not file:
        app.logger.info("No file provided in request")
        return jsonify({"error": "No file provided"}), 400

    app.logger.info(f"Received file: {file.filename}")
    s3_client.upload_fileobj(file, MINIO_BUCKET, file.filename)
    return jsonify({"message": f"File {file.filename} uploaded successfully!"}), 200

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    # Extract Authorization header (JWT token)
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing authorization token"}), 401
    token = token.split(" ")[1]  # Assuming Bearer token format

    # Validate the token
    decoded_token = validate_jwt(token)
    if not decoded_token:
        return jsonify({"error": "Invalid or expired token"}), 401

    try:
        file_obj = s3_client.get_object(Bucket=MINIO_BUCKET, Key=file_id)
        return file_obj['Body'].read(), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/update/<file_id>', methods=['PUT'])
def update_file(file_id):
    # Extract Authorization header (JWT token)
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing authorization token"}), 401
    token = token.split(" ")[1]  # Assuming Bearer token format

    # Validate the token
    decoded_token = validate_jwt(token)
    if not decoded_token:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Proceed with the file update
    file = request.files['file']
    s3_client.upload_fileobj(file, MINIO_BUCKET, file_id)
    return jsonify({"message": f"File {file_id} updated successfully!"}), 200

@app.route('/delete/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    # Extract Authorization header (JWT token)
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing authorization token"}), 401
    token = token.split(" ")[1]  # Assuming Bearer token format

    # Validate the token
    decoded_token = validate_jwt(token)
    if not decoded_token:
        return jsonify({"error": "Invalid or expired token"}), 401

    try:
        s3_client.delete_object(Bucket=MINIO_BUCKET, Key=file_id)
        return jsonify({"message": f"File {file_id} deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
