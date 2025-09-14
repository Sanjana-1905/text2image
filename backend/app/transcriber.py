from faster_whisper import WhisperModel

# Configuration
MODEL_SIZE = "medium"       # Options: tiny, base, small, medium, large
DEVICE = "cpu"
COMPUTE_TYPE = "int8"      # Use 'int8' for lower memory & faster CPU inference

# Initialize the Whisper model once
model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

def transcribe(audio_path: str, language: str | None = None) -> str:
    """
    Transcribe an audio file into text.
    
    Args:
        audio_path (str): Path to the input audio file (.webm, .wav, etc.).
        language (str | None): Optional language hint (e.g., 'en' for English).
    
    Returns:
        str: Concatenated transcription text of the entire audio.
    """
    segments, _info = model.transcribe(audio_path, language=language)

    # Collect and clean up segment texts
    text = " ".join(segment.text.strip() for segment in segments if segment.text.strip())

    return text