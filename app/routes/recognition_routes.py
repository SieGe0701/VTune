from flask import Blueprint, request, jsonify, render_template
from utils.song_recognition import recognize_song
import os
from utils.song_info import extract_song_info
recognition_routes = Blueprint("recognition_routes", __name__)

# Define the path where uploaded files will be temporarily stored
UPLOAD_FOLDER = "data/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@recognition_routes.route("/recognize", methods=["POST"])
def recognize():
    """
    Route to recognize a song from an uploaded file.
    """
    try:
        # Check if a file is present in the request
        if "audio" not in request.files:
            return render_template("result.html", match=None, error="No file part in the request"), 400
        
        file = request.files["audio"]
        
        # Check if the file is empty
        if file.filename == "":
            return render_template("result.html", match=None, error="No file selected"), 400
        
        # Save the uploaded file to the server
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Use the recognition function to identify the song
        result = recognize_song(file_path)

        # Clean up the uploaded file after processing
        os.remove(file_path)

        # Handle the result
        if "error" in result:
             return render_template("result.html", match=None, error=result["error"]), 500
        
        # Parse and structure the response
        if result.get("status", {}).get("code") == 0:  # Success case
            song_info = extract_song_info(result)
            return render_template("result.html", match=song_info), 200

        # No match found or other status code
        return render_template("result.html", match=None, error="No match found"), 404

    except Exception as e:
        return render_template("result.html", match=None, error=f"An unexpected error occurred: {str(e)}"), 500

@recognition_routes.route("/", methods=["GET"])
def index():
    """
    Route for the home page.
    """
    return render_template("index.html")
