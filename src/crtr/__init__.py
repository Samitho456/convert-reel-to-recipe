"""
CRTR (Convert Reel To Recipe)
A Python package for converting Instagram cooking reels into structured recipes.
"""

from .converter import ConvertReelToRecipe
from .transcribe_audio import TranscribeAudio, ModelSize
from .generate_recipe_with_ai import generate_recipe_with_gemini, GeminiModel

__version__ = "0.1.0"
__all__ = [
    "ConvertReelToRecipe",
    "TranscribeAudio",
    "ModelSize",
    "generate_recipe_with_gemini",
    "GeminiModel",
]
