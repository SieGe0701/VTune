# Vtune App

## Overview
The "Vtune" app allows users to hum a tune or upload an audio file, and the app identifies the song by comparing it against a database of song features.

---

## Features
1. Upload or hum a tune for song identification.
2. Displays the name, artist, and metadata of the matched song.
3. Easy to expand the database by preprocessing new songs.

---

## Prerequisites

### 1. System Requirements
- Python 3.8 or later
- Pip (Python package manager)
- Flask
- An internet browser for accessing the app

### 2. Install Dependencies
Install the required Python libraries using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## Running the App

### 1. Clone the Repository
Clone the project repository or ensure you have the project folder structure as outlined.

```bash
git clone <repository-url>
cd vtune
```

### 2. Preprocess Songs
If you have new songs to add to the database:
- Place them in the `data/songs/` directory.
- Run the preprocessing script:

```bash
python scripts/audio_preprocessor.py
```

This will extract features from the songs and update the `data/song_metadata.json` file.

### 3. Start the Flask App
Navigate to the `app/` directory and run the Flask app:

```bash
python main.py
```

You should see an output similar to:

```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### 4. Access the App
Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Usage

### 1. Upload a Tune
- Click the "Choose File" button and select an audio file (e.g., `.mp3`, `.wav`).
- Click "Identify Song."

### 2. View the Result
- The app will display the matched song title, artist, and any additional metadata.

---

## License
This project is open-source. Feel free to modify and share as needed.



