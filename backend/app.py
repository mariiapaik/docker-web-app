from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from db import db
from models import Message
import os

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db/messages_db")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/messages", methods=["POST"])
def create_message():
    data = request.get_json()
    if "text" not in data:
        return jsonify({"error": "Missing text"}), 400

    new_message = Message(text=data["text"])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"id": new_message.id, "text": new_message.text}), 201

@app.route("/messages", methods=["GET"])
def get_messages():
    messages = Message.query.all()
    return jsonify([{"id": msg.id, "text": msg.text} for msg in messages])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
