from flask import Blueprint, request, jsonify, redirect, session, url_for
from backend.utils.ml_model import SentimentModel
from backend.utils.youtube import upload_video, get_flow, credentials_to_dict, dict_to_credentials
import os
import requests
import uuid

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

sentiment_model = SentimentModel()
routes = Blueprint('routes', __name__)

# In-memory storage untuk credentials (sederhana untuk single instance)
# Format: { 'session_id': credentials_dict }
USER_CREDENTIALS = {} 

@routes.route('/auth/url')
def auth_url():
    """Generate link login Google"""
    flow = get_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    # Simpan state di session jika perlu validasi CSRF
    return jsonify({"url": authorization_url})

@routes.route('/auth/callback')
def auth_callback():
    """Callback dari Google setelah user login"""
    code = request.args.get('code')
    if not code:
        return "Missing code", 400
    
    try:
        flow = get_flow()
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Simpan credentials ke in-memory store dengan ID unik
        session_id = str(uuid.uuid4())
        USER_CREDENTIALS[session_id] = credentials_to_dict(credentials)
        
        # Redirect kembali ke Frontend dengan token
        return redirect(f"http://localhost:30080?token={session_id}")
    except Exception as e:
        return f"Auth Error: {str(e)}", 500

@routes.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({"error": "No video file"}), 400

    video = request.files['video']
    title = request.form.get('title', '')
    description = request.form.get('description', '')
    email = request.form.get('email', '')
    token = request.form.get('token', '')

    # Validasi Login
    if not token or token not in USER_CREDENTIALS:
        return jsonify({"error": "Unauthorized. Please connect YouTube account first."}), 401
    
    # Ambil credentials user
    creds_dict = USER_CREDENTIALS[token]
    credentials = dict_to_credentials(creds_dict)

    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)

    try:
        # sentiment_model.predict now returns a dict
        prediction = sentiment_model.predict(title, description)
        sentiment = prediction["label"]
        confidence = prediction["confidence"]
        keywords = prediction["keywords"]
        category = prediction.get("category", "Umum")

        youtube_link = None
        upload_error = None

        try:
            # Upload menggunakan credentials user
            yt_data = upload_video(credentials, video_path, title, description)
            youtube_link = yt_data["url"]
        except Exception as e:
            print("❌ YouTube Upload Error (Skipping but continuing):", e)
            upload_error = str(e)
            youtube_link = "https://youtube.com/failed_upload_placeholder"

        n8n_webhook = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/send_notification")
        payload = {
            "email": email,
            "title": title,
            "sentiment": sentiment,
            "confidence": confidence,
            "keywords": keywords,
            "category": category,
            "youtube_link": youtube_link,
            "upload_status": "failed" if upload_error else "success",
            "upload_error": upload_error
        }

        try:
            print("🔹 Sending to n8n webhook:", payload)
            res = requests.post(n8n_webhook, json=payload)
            print("🔹 n8n response:", res.status_code, res.text)
        except Exception as e:
            print("❌ n8n webhook error:", e)

        response_data = {
            "message": "Processed successfully!",
            "youtube_link": youtube_link,
            "sentiment": sentiment,
            "confidence": confidence,
            "keywords": keywords,
            "category": category
        }

        if upload_error:
            response_data["warning"] = "YouTube upload failed, but analysis was completed."
            response_data["upload_error"] = upload_error

        return jsonify(response_data)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e), "details": traceback.format_exc()}), 500
