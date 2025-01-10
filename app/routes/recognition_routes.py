from flask import Blueprint, request, jsonify, render_template
from utils.song_recognition import recognize_song
import base64
import os
from utils.song_info import extract_song_info
recognition_routes = Blueprint("recognition_routes", __name__)

# Define the path where uploaded files will be temporarily stored
UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@recognition_routes.route("/recognize", methods=["POST"])
def recognize():
    """
    Route to recognize a song from an uploaded file or a recorded audio input.
    """
    try:
        # Handle audio file upload
        if "audio" in request.files:
            file = request.files["audio"]
            if file.filename == "":
                return render_template("result.html", match=None, error="No file selected"), 400

            # Save the uploaded file temporarily and recognize
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            result = recognize_song(file_path)
            os.remove(file_path)

        # Handle base64-encoded recorded audio from the form
        elif "recorded_audio" in request.form:
            recorded_audio = request.form["recorded_audio"]
            header, encoded = recorded_audio.split(",", 1)
            audio_data = base64.b64decode(encoded)

            # Save the decoded audio to a temporary file
            temp_file_path = os.path.join(UPLOAD_FOLDER, "recorded_audio.webm")
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(audio_data)

            # Recognize the recorded audio
            result = recognize_song(temp_file_path)
            os.remove(temp_file_path)

        else:
            return render_template("result.html", match=None, error="No audio data provided"), 400

        # Process the result from the recognition function
        if result.get("status", {}).get("code") == 0:  # Success
            song_info = extract_song_info(result)
            return render_template("result.html", match=song_info), 200

        # No match or other issue
        return render_template("result.html", match=None, error="No match found"), 404

    except Exception as e:
        # Handle unexpected errors
        return render_template("result.html", match=None, error=f"An unexpected error occurred: {str(e)}"), 500


