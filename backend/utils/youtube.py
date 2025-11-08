import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scope untuk upload video ke YouTube
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# File konfigurasi
CLIENT_SECRETS_FILE = "backend/client_secrets.json"
TOKEN_PICKLE = "backend/token.pickle"

def upload_video(file_path, title, description):
    creds = None

    # Jika token sebelumnya ada, gunakan
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, "rb") as token:
            creds = pickle.load(token)

    # Jika belum ada token atau tidak valid, lakukan autentikasi
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Gunakan port tetap supaya redirect_uri tidak berubah-ubah
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                SCOPES
            )
            creds = flow.run_local_server(
                port=8080,            # pakai port tetap
                redirect_uri_trusted=True
            )

        # Simpan token agar tidak perlu login lagi
        with open(TOKEN_PICKLE, "wb") as token:
            pickle.dump(creds, token)

    # Build service YouTube
    youtube = build("youtube", "v3", credentials=creds)

    # Upload video
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["SmartUploader", "AutoUpload", "ML"]
            },
            "status": {"privacyStatus": "private"}  # Bisa diubah ke 'public'
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
