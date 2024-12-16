import json
import librosa
import numpy as np

def extract_features(audio_path):
    """
    Extract combined features for songs in the database.
    """
    y, sr = librosa.load(audio_path, sr=16000)

    # MFCC Features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_mean = mfcc.mean(axis=1)

    # Chroma Features
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)

    # Combine MFCC and Chroma features
    combined_features = np.concatenate((mfcc_mean, chroma_mean))

    # Convert to a Python list for JSON serialization
    return combined_features.tolist()



def preprocess_songs(metadata_file):
    """
    Preprocess all songs in the metadata file and save their features.
    """
    with open(metadata_file, 'r') as file:
        songs = json.load(file)

    for song in songs:
        print(f"Processing: {song['title']} by {song['artist']}")
        song['features'] = extract_features(song['audio_file'])

    # Save updated metadata
    with open(metadata_file, 'w') as file:
        json.dump(songs, file, indent=4)

if __name__ == "__main__":
    preprocess_songs("data/song_metadata.json")
