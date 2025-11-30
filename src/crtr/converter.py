"""Main converter class for transforming Instagram reels into recipes."""

import json
import os
import re
import requests
import instaloader

from . import prompt
from . import generate_recipe_with_ai
from . import convert_video_to_audio
from . import transcribe_audio


class ConvertReelToRecipe:
    """
    A class for downloading Instagram reels and converting them into structured recipes.
    
    This class handles the full pipeline: downloading the reel, extracting audio,
    transcribing the audio, and generating a recipe using AI.
    """
    
    def __init__(self):
        """Initialize the converter with default settings."""
        # Store the prompt template from prompt.py
        self.prompt_template = prompt.RECIPE_GENERATION_PROMPT
        self.prompt = None  # Will hold the last formatted prompt
        self.transcript = None
        self.description = None
        self.shortcode = None
        
    def download_reel_from_shortcode(self, shortcode):
        """
        Downloads an Instagram Reel video using its shortcode.
        
        Args:
            shortcode: Instagram post shortcode (e.g., 'ABC123xyz')
            
        Returns:
            str: Path to the downloaded video file, or None if failed
        """
        L = instaloader.Instaloader()
        try:
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            if not post.is_video or not post.video_url:
                print(f"Error: Post {shortcode} is not a video or has no video URL")
                return None
                
            video_url = post.video_url
            self.description = post.caption
            headers = {'User-Agent': 'Mozilla/5.0'} 
            response = requests.get(video_url, stream=True, headers=headers)
            
            if response.status_code == 200:
                filename = f"{shortcode}.mp4"
                with open(filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                        if chunk:
                            file.write(chunk)
                return filename
            else:
                print(f"Error: Failed to download video (status code: {response.status_code})")
                return None
                
        except Exception as e:
            print(f"Error downloading reel: {e}")
            return None
        
    def convert_to_recipe_from_reel_url(self, reel_url, ai_model=None, api_key=None):
        """
        Full pipeline: download reel, convert to audio, transcribe, build prompt, generate recipe.
        
        Args:
            reel_url: Instagram reel URL or shortcode
            ai_model: AI model to use (default: Gemini 2.0 Flash)
            api_key: API key for the AI service
            
        Returns:
            str: Generated recipe text (JSON format), or None if failed
        """
        shortcode = self.extract_shortcode(reel_url)
        video_path = self.download_reel_from_shortcode(shortcode)
        if not video_path:
            return None
            
        audio_path = self.convert_video_to_audio(video_path)
        transcript = self.transcribe_audio(audio_path)
        self.build_prompt(description=self.description, transcript=transcript)
        recipe_text = self.generate_recipe(ai_model=ai_model, api_key=api_key)
        return recipe_text
    
    def get_audio_from_url(self, url):
        """
        Downloads audio from a given video URL.
        
        Args:
            url: Instagram reel URL or shortcode
            
        Returns:
            str: Path to the extracted audio file, or None if failed
        """
        video_path = self.download_reel_from_shortcode(self.extract_shortcode(url))
        if not video_path:
            return None
        audio_path = self.convert_video_to_audio(video_path)
        return audio_path
    
    def transcribe_audio(self, audio_path):
        """
        Transcribes audio from a given audio file path.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        ta = transcribe_audio.TranscribeAudio(
            model_size=transcribe_audio.ModelSize.MEDIUM.value
        )
        transcription = ta.transcribe(audio_path)
        self.transcript = transcription
        
        # Clean up audio file after transcription
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        return transcription
    
    def build_prompt(self, description: str, transcript: str) -> str:
        """
        Format the recipe generation prompt with description and transcript.
        
        Args:
            description: Instagram reel description/caption
            transcript: Transcribed audio text
            
        Returns:
            str: Formatted prompt ready for AI
        """
        formatted = self.prompt_template.format(
            description=description.strip(),
            transcript=transcript.strip()
        )
        self.prompt = formatted
        return formatted

    def generate_recipe(self, ai_model=None, api_key=None):
        """
        Generates a recipe JSON string based on transcript and description.
        
        Args:
            ai_model: AI model identifier
            api_key: API key for the AI service
            
        Returns:
            str: Generated recipe in JSON format, or None if failed
        """
        if not ai_model or not api_key:
            print("Error: AI Model or API Key not configured.")
            return None
            
        recipe_text = generate_recipe_with_ai.generate_recipe_with_gemini(
            prompt=self.prompt,
            api_key=api_key,
            model=ai_model
        )
        
        if not recipe_text:
            return None
        
        # Try to save as JSON
        try:
            recipe_json = json.loads(recipe_text)
            # Save as formatted JSON file
            output_filename = f"{self.shortcode}.json"
            with open(output_filename, "w", encoding="utf-8") as f:
                json.dump(recipe_json, f, ensure_ascii=False, indent=2)
            print(f"Recipe saved to {output_filename}")
        except json.JSONDecodeError as e:
            print(f"Warning: AI output is not valid JSON: {e}")
            # Fallback: save as text file
            output_filename = f"{self.shortcode}_raw.txt"
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(recipe_text)
            print(f"Raw output saved to {output_filename}")
        
        return recipe_text
    
    def convert_video_to_audio(self, video_path):
        """
        Converts a video file to an audio file by extracting the audio track.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            str: Path to the extracted audio file
        """
        audio_path = video_path.rsplit('.', 1)[0] + '.mp3'
        convert_video_to_audio.convert_mp4_to_mp3(video_path, audio_path)
        return audio_path
    
    def extract_shortcode(self, url_or_code):
        """
        Return an Instagram shortcode from a full URL or plain shortcode.

        Handles shared URLs that include query parameters (e.g. ?utm_source=...) and
        common path formats like /reel/<shortcode>/, /p/<shortcode>/, /tv/<shortcode>/.
        If the input is already a shortcode (no slashes), it's returned as-is.
        
        Args:
            url_or_code: Instagram URL or shortcode
            
        Returns:
            str: Extracted shortcode
        """
        if not url_or_code:
            return ""

        s = url_or_code.strip()
        # If it's already a shortcode (no slash, no ://)
        if "://" not in s and "/" not in s:
            self.shortcode = s
            return s

        # Regex to capture shortcode from reel/p/tv URL formats
        match = re.search(r'/(?:reel|p|tv)/([^/?#]+)', s)
        if match:
            self.shortcode = match.group(1)
            return match.group(1)

        # Fallback: last non-empty path segment (skip domain)
        match = re.search(r'instagram\.com/([^/?#]+)', s)
        if match:
            self.shortcode = match.group(1)
            return match.group(1)

        # Final fallback: return as-is
        self.shortcode = s
        return s
    
    def get_prompt(self):
        """
        Get the last formatted prompt.
        
        Returns:
            str: The formatted prompt, or None if not yet built
        """
        return self.prompt
