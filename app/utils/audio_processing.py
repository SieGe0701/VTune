from pydub import AudioSegment

def process_audio(audio_file):
    """
    Processes the uploaded audio file.
    - Converts to mono
    - Sets a consistent frame rate of 16000 Hz
    """
    # Read the file-like object directly
    audio = AudioSegment.from_file(audio_file.stream)
    audio = audio.set_frame_rate(16000).set_channels(1)
    return audio
