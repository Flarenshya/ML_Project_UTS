from flask import Blueprint, request, jsonify
from backend.utils.ml_model import SentimentModel
from backend.utils.youtube import upload_video
import os
import requests

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

sentiment_model = SentimentModel()
routes = Blueprint('routes', __name__)

@routes.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({"error": "No video file"}), 400

    video = request.files['video']
    title = request.form.get('title', '')
    description = request.form.get('description', '')
    email = request.form.get('email', '')

    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)

    sentiment = sentiment_model.predict(title, description)

    yt_data = upload_video(video_path, title, description)
    youtube_link = yt_data["url"]

    n8n_webhook = "http://localhost:5678/webhook/send_notification"
    payload = {
        "email": email,
        "title": title,
        "sentiment": sentiment,
        "youtube_link": youtube_link
    }

    try:
        print("🔹 Sending to n8n webhook:", payload)
        res = requests.post(n8n_webhook, json=payload)
        print("🔹 n8n response:", res.status_code, res.text)
    except Exception as e:
        print("❌ n8n webhook error:", e)

    return jsonify({
        "message": "Upload success!",
        "youtube_link": youtube_link,
        "sentiment": sentiment
    })
