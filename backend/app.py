from flask import Flask
from flask_cors import CORS
from backend.routes import routes

app = Flask(__name__)
app.secret_key = "secret_key_secure_random" # Ganti dengan yang lebih aman di production
CORS(app) 
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
