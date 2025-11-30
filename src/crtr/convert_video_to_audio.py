"""Audio conversion module for extracting audio from video files."""

import os
from moviepy import VideoFileClip


def convert_mp4_to_mp3(input_path, output_path=None):
    """
    Converts an MP4 video file to an MP3 audio file by extracting the audio track.
    
    Args:
        input_path: Path to the input MP4 video file
        output_path: Path to save the output MP3 audio file (optional)
    
    Raises:
        FileNotFoundError: If the input file doesn't exist
        Exception: If audio extraction fails
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at '{input_path}'")

    if output_path is None:
        output_path = input_path.rsplit('.', 1)[0] + '.mp3'

    print(f"Loading video: {input_path}")
    try:
        # Load the video file
        video_clip = VideoFileClip(input_path)
        
        # Extract the audio component
        audio_clip = video_clip.audio
        
        if audio_clip is None:
            raise ValueError("No audio track found in video")
        
        audio_clip.write_audiofile(output_path, codec='mp3', logger=None)
        
        # Clean up resources
        audio_clip.close()
        video_clip.close()
        
        print(f"✅ Audio extraction successful! File saved as {os.path.abspath(output_path)}")
        
        # Remove the original video file
        if os.path.exists(input_path):
            os.remove(input_path)

    except Exception as e:
        print(f"❌ An error occurred during audio extraction: {e}")
        print("Tip: If you see a 'No ffmpeg exe could be found' error, you may need to install FFmpeg separately on your system.")
        raise
