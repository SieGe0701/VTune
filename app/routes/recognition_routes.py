from flask import Blueprint, request, jsonify
from utils.audio_processing import process_audio

recognition = Blueprint('recognition', __name__)

@recognition.route('/recognize', methods=['POST'])
def recognize():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files['audio']  # Get the uploaded file

    try:
        # Process the uploaded audio directly
        audio = process_audio(audio_file)

        # Placeholder for recognition logic
        return jsonify({"message": "Audio processed successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
