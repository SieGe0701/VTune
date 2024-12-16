from flask import Blueprint, request, jsonify
from utils.audio_processing import process_audio
from utils.song_recognition import extract_features_from_hum, recognize_song

recognition = Blueprint('recognition', __name__)

@recognition.route('/recognize', methods=['POST'])
def recognize():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files['audio']

    try:
        # Process the hummed audio
        audio = process_audio(audio_file)
        hummed_features = extract_features_from_hum(audio)

        # Match with song database
        result = recognize_song(hummed_features, "data/song_metadata.json")

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
