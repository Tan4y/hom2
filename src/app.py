# Import Flask framework for building the web app
from flask import Flask, request, jsonify
# Import boto3 for interacting with AWS and MinIO services
import boto3
# Import jwt for handling JSON Web Tokens
import jwt
# Import configuration variables for MinIO and Keycloak
from config import MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET
from config import KEYCLOAK_CLIENT_ID, KEYCLOAK_PUBLIC_KEY

# Initialize Flask application
app = Flask(__name__)

# Configure MinIO client with credentials and endpoint
s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1"
)

# List and print available MinIO buckets during initialization
buckets = s3_client.list_buckets()
print("Buckets:", buckets)

# Function to validate a JWT token using Keycloak's public key
def validate_jwt(token):
    try:
        # Decode the JWT and verify its audience and signature
        decoded_token = jwt.decode(token, KEYCLOAK_PUBLIC_KEY, algorithms=["RS256"], audience=KEYCLOAK_CLIENT_ID)
        return decoded_token
    except jwt.ExpiredSignatureError:
        # Return None if the token is expired
        return None
    except jwt.InvalidTokenError:
        # Return None if the token is invalid
        return None

# Route for the API index, providing usage instructions
@app.route('/')
def index():
    return 'Welcome to the File Management API! Visit /upload to upload a file, /download/<file_id> to download a file, /update/<file_id> to update a file, and /delete/<file_id> to delete a file.'

# Route for uploading files to MinIO
@app.route('/upload', methods=['POST'])
def upload_file():
    # Extract Authorization header for JWT
    token = request.headers.get("Authorization")
    if not token:
        app.logger.info("Missing authorization token")
        return jsonify({"error": "Missing authorization token"}), 401
    token = token.split(" ")[1]  # Extract the actual token from Bearer format

    # Validate the provided JWT
    decoded_token = validate_jwt(token)
    if not decoded_token:
        app.logger.info("Invalid or expired token")
        return jsonify({"error": "Invalid or expired token"}), 401

    # Check if a file is included in the request
    file = request.files.get('file')
    if not file:
        app.logger.info("No file provided in request")
        return jsonify({"error": "No file provided"}), 400

    # Upload the file to MinIO
    app.logger.info(f"Received file: {file.filename}")
    s3_client.upload_fileobj(file, MINIO_BUCKET, file.filename)
    return jsonify({"message": f"File {file.filename} uploaded successfully!"}), 200

# Route for downloading files from MinIO
@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    # Extract Authorization header for JWT
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing authorization token"}), 401
    token = token.split(" ")[1]  # Extract the actual token from Bearer format

    # Validate the provided JWT
    decoded_token = validate_jwt(token)
    if not decoded_token:
        return jsonify({"error": "Invalid or expired token"}), 401

    try:
        # Attempt to retrieve the file from MinIO
        file_obj = s3_client.get_object(Bucket=MINIO_BUCKET, Key=file_id)
        return file_obj['Body'].read(), 200
    except Exception as e:
        # Return an error if the file is not found
        return jsonify({"error": str(e)}), 404

# Route for updating files in MinIO
@app.route('/update/<file_id>', methods=['PUT'])
def update_file(file_id):
    # Extract Authorization header for JWT
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing authorization token"}), 401
    token = token.split(" ")[1]  # Extract the actual token from Bearer format

    # Validate the provided JWT
    decoded_token = validate_jwt(token)
    if not decoded_token:
        return jsonify({"error": "Invalid or expired token"}), 401

    # Update the file in MinIO
    file = request.files['file']
    s3_client.upload_fileobj(file, MINIO_BUCKET, file_id)
    return jsonify({"message": f"File {file_id} updated successfully!"}), 200

# Route for deleting files from MinIO
@app.route('/delete/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    # Extract Authorization header for JWT
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing authorization token"}), 401
    token = token.split(" ")[1]  # Extract the actual token from Bearer format

    # Validate the provided JWT
    decoded_token = validate_jwt(token)
    if not decoded_token:
        return jsonify({"error": "Invalid or expired token"}), 401

    try:
        # Attempt to delete the file from MinIO
        s3_client.delete_object(Bucket=MINIO_BUCKET, Key=file_id)
        return jsonify({"message": f"File {file_id} deleted successfully!"}), 200
    except Exception as e:
        # Return an error if the file cannot be deleted
        return jsonify({"error": str(e)}), 404

# Run the Flask app on the specified host and port
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002)
