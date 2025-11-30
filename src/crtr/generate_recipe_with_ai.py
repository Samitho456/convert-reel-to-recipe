"""AI recipe generation module using Google's Gemini API."""

import enum
from google import genai


class GeminiModel(enum.Enum):
    """Available Gemini AI models for recipe generation."""
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_2_5_FLASH_LITE = "gemini-2.5-flash-lite"


def generate_recipe_with_gemini(prompt, api_key, model=GeminiModel.GEMINI_2_0_FLASH.value):
    """
    Calls the Gemini API with the provided prompt and returns the generated recipe text.
    
    Args:
        prompt: The formatted prompt containing recipe instructions
        api_key: Google AI API key
        model: Model identifier (default: gemini-2.0-flash)
    
    Returns:
        str: Generated recipe text in JSON format, or None if failed
    """
    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )
        return getattr(response, "text", str(response))
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return None
