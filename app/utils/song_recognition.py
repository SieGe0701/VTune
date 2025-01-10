import base64
import hashlib
import hmac
import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load ACRCloud credentials from .env file
host = os.getenv("host")
access_key = os.getenv("access_key")
access_secret = os.getenv("secret_key")

if not host or not access_key or not access_secret:
    raise ValueError("Missing required ACRCloud credentials in .env file.")

# API details
requrl = f"https://{host}/v1/identify"
http_method = "POST"
http_uri = "/v1/identify"
data_type = "audio"
signature_version = "1"

def recognize_song(file_path):
    """Recognize a song using the ACRCloud API."""
    try:
        # Generate timestamp and signature
        timestamp = str(int(time.time()))
        string_to_sign = f"{http_method}\n{http_uri}\n{access_key}\n{data_type}\n{signature_version}\n{timestamp}"
        sign = base64.b64encode(
            hmac.new(access_secret.encode('ascii'), string_to_sign.encode('ascii'), digestmod=hashlib.sha1).digest()
        ).decode('ascii')

        # Get file size and prepare request payload
        sample_bytes = os.path.getsize(file_path)
        with open(file_path, "rb") as f:
            files = [('sample', (os.path.basename(file_path), f, 'audio/mpeg'))]
            data = {
                'access_key': access_key,
                'sample_bytes': sample_bytes,
                'timestamp': timestamp,
                'signature': sign,
                'data_type': data_type,
                "signature_version": signature_version
            }

            # Send request to ACRCloud
            response = requests.post(requrl, files=files, data=data)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()  # Parse and return JSON response

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

