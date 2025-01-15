MINIO_URL = "http://minio:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_BUCKET = "file-storage"

# Keycloak Configuration
KEYCLOAK_URL = "http://keycloak:8080"
REALM = "file-management"
KEYCLOAK_CLIENT_ID = "file-client"
KEYCLOAK_CLIENT_SECRET = "xwyK7plDqsqZ7dyfqee1PLqhLacWmfdh"

# Add Keycloak public key for JWT verification
KEYCLOAK_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxQ7Yu4SbZfp/AOsJPlAQDORuakmZS9BtxzKwo9x3fPKbu1cUfcvqCObMTd6Lge3jUEpIm2GDRIL1fTf1lIFbXKQvaC5rjUlw/sCDBqFuwixV/oA6BoYAsRhZvlsiN+xhj2D6SvFq12C7Dkmsg9g1Xnl8GbNRdEVWAbd+25tzpc6zXhJrHOPlMEJiig+gPOthzQWcqTksC+wammDLk/MVXsDB2exT/foUL4yMumvH5tmMA7+fIN7WLeVu4Vy6vmVpOWVSq0nrFhfIyBAzoFEznoy55qniRAZ+F3ZyI8N0I1UtuuQhtEleFtZ13MLOpyAEjHdw0KvFO5yt+1+xA0hOaQIDAQAB
-----END PUBLIC KEY-----
"""
