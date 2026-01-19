import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import google.oauth2.credentials

# Scope untuk upload video ke YouTube
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# File konfigurasi
CLIENT_SECRETS_FILE = "backend/client_secrets.json"

def get_flow():
    """Membuat objek Flow untuk OAuth Web Server"""
    # Gunakan ENV variable agar fleksibel (bisa 5000, 30080, atau domain asli)
    redirect_uri = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:30080/auth/callback")
    
    return Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=redirect_uri 
    )

def credentials_to_dict(credentials):
    """Mengubah object Credentials menjadi dictionary agar bisa disimpan"""
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def dict_to_credentials(cred_dict):
    """Mengubah dictionary kembali menjadi object Credentials"""
    return google.oauth2.credentials.Credentials(**cred_dict)

def upload_video(credentials, file_path, title, description):
    """Upload video menggunakan credentials yang diberikan"""
    
    # Build service YouTube dengan credentials user
    youtube = build("youtube", "v3", credentials=credentials)

    # Upload video
    print(f"Uploading video: {title}...")
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["SmartUploader", "AutoUpload", "ML"]
            },
            "status": {"privacyStatus": "private"}  # Default private
        },
        media_body=MediaFileUpload(file_path)
    )

    response = request.execute()

    # Return hasil upload
    return {
        "id": response["id"],
        "title": title,
        "url": f"https://youtu.be/{response['id']}"
    }
