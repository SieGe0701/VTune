import json
import numpy as np
import librosa

def extract_features_from_hum(audio):
    """
    Extract combined features from the user's hummed audio.
    """
    y = np.array(audio.get_array_of_samples(), dtype=np.float32) / 32768.0
    sr = audio.frame_rate

    # Extract MFCC features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_mean = mfcc.mean(axis=1)

    # Extract Chroma features
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)

    # Combine MFCC and Chroma features
    combined_features = np.concatenate((mfcc_mean, chroma_mean))
    return combined_features

def recognize_song(hummed_features, metadata_file, threshold=0.75):
    """
    Match the hummed features with the song database.
    """
    with open(metadata_file, 'r') as file:
        songs = json.load(file)

    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    best_match = None
    best_score = -1

    for song in songs:
        # Convert stored features (list) to a NumPy array
        song_features = np.array(song['features'])
        similarity = cosine_similarity(hummed_features, song_features)
    

        if similarity > best_score:
            best_score = similarity
            best_match = song

    if best_match and best_score >= threshold:
        return {
            "title": best_match['title'],
            "artist": best_match['artist'],
            "score": best_score
        }
    else:
        return {"error": "No match found above the threshold"}



def normalize_features(features):
    """
    Normalize features to have zero mean and unit variance.
    """
    return (features - np.mean(features)) / np.std(features)
