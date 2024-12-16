import unittest
import numpy as np
from app.utils.song_recognition import recognize_song, normalize_features

class TestSongRecognition(unittest.TestCase):
    def test_similarity_metric(self):
        features1 = np.array([1, 2, 3])
        features2 = np.array([1, 2, 3])
        features3 = np.array([4, 5, 6])

        self.assertAlmostEqual(cosine_similarity(features1, features2), 1.0)
        self.assertLess(cosine_similarity(features1, features3), 1.0)

    def test_recognition(self):
        hummed_features = np.array([...])  # Provide test hummed feature vector
        result = recognize_song(hummed_features, "data/song_metadata.json")
        self.assertIn("title", result)

if __name__ == "__main__":
    unittest.main()
