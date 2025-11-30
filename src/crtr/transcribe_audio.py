"""Audio transcription module using Whisper AI."""

import enum
import torch
from faster_whisper import WhisperModel


class ModelSize(enum.Enum):
    """Available Whisper model sizes."""
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE_V3 = "large-v3"


class TranscribeAudio:
    """
    A class for transcribing audio files using OpenAI's Whisper model.
    
    Automatically detects and uses CUDA if available, otherwise falls back to CPU.
    """
    
    def __init__(self, model_size=ModelSize.MEDIUM.value):
        """
        Initialize the transcription model.
        
        Args:
            model_size: Whisper model size to use (default: medium)
        """
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Initializing Whisper model ({model_size}) on {device}...")
        self.model = WhisperModel(model_size, device=device)

    def transcribe(self, file_path):
        """
        Transcribes the audio file at the given file path using the Whisper model.
        
        Args:
            file_path: The path to the audio file to be transcribed
        
        Returns:
            str: The transcribed text from the audio
        """
        transcript = ""
        result = self.model.transcribe(file_path, beam_size=5)
    
        # Unpack if tuple (segments, info)
        if isinstance(result, tuple) and len(result) >= 1:
            segments = result[0]
        else:
            segments = result
            
        # Some implementations return a generator; iterate and collect text safely
        for seg in segments:
            # seg is expected to have a .text attribute; fallback to dict access
            text = getattr(seg, "text", None)
            if text is None and isinstance(seg, dict):
                text = seg.get("text")
            if text:
                transcript += text + " "

        return transcript.strip()
