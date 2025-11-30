# CRTR - Convert Reel To Recipe

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Convert Instagram cooking reels into structured, nutritionally-analyzed recipes using AI.

## Features

- 📥 Download Instagram reels directly from URLs or shortcodes
- 🎵 Extract audio from video files
- 🎤 Transcribe audio using OpenAI's Whisper model
- 🤖 Generate structured recipes with Google's Gemini AI
- 🇩🇰 Outputs recipes in Danish with metric measurements
- 📊 Includes nutritional analysis
- 💾 Saves recipes as formatted JSON files

## Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (required for video/audio processing)

#### Installing FFmpeg

**Windows:**

```powershell
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**macOS:**

```bash
brew install ffmpeg
```

**Linux:**

```bash
sudo apt-get install ffmpeg  # Debian/Ubuntu
sudo yum install ffmpeg      # CentOS/RHEL
```

### Install CRTR

#### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/crtr.git
cd crtr

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

#### From PyPI (once published)

```bash
pip install crtr
```

## Quick Start

### Basic Usage

```python
from crtr import ConvertReelToRecipe, GeminiModel

# Initialize the converter
converter = ConvertReelToRecipe()

# Convert a reel to a recipe
recipe = converter.convert_to_recipe_from_reel_url(
    reel_url="https://www.instagram.com/reel/ABC123xyz/",
    ai_model=GeminiModel.GEMINI_2_0_FLASH.value,
    api_key="your-google-ai-api-key"
)

print(recipe)  # Outputs JSON-formatted recipe
```

### Step-by-Step Usage

```python
from crtr import ConvertReelToRecipe, TranscribeAudio, ModelSize

converter = ConvertReelToRecipe()

# 1. Download the reel
shortcode = converter.extract_shortcode("https://www.instagram.com/reel/ABC123xyz/")
video_path = converter.download_reel_from_shortcode(shortcode)

# 2. Extract audio
audio_path = converter.convert_video_to_audio(video_path)

# 3. Transcribe audio
transcript = converter.transcribe_audio(audio_path)

# 4. Build the AI prompt
prompt = converter.build_prompt(
    description=converter.description,
    transcript=transcript
)

# 5. Generate recipe
recipe = converter.generate_recipe(
    ai_model="gemini-2.0-flash",
    api_key="your-api-key"
)
```

## Configuration

### API Keys

You'll need a Google AI API key to use the recipe generation feature:

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Use it in your code or set as environment variable:

```bash
export GOOGLE_AI_API_KEY="your-key-here"
```

### Model Selection

CRTR supports multiple AI models:

```python
from crtr import GeminiModel

# Available models
GeminiModel.GEMINI_2_0_FLASH.value       # Fast, recommended
GeminiModel.GEMINI_2_5_FLASH_LITE.value  # Lightweight
```

For transcription, choose from different Whisper model sizes:

```python
from crtr import ModelSize

# Available sizes (larger = more accurate but slower)
ModelSize.TINY.value
ModelSize.BASE.value
ModelSize.SMALL.value
ModelSize.MEDIUM.value    # Default
ModelSize.LARGE_V3.value
```

## Output Format

Recipes are generated as JSON with the following structure:

```json
{
  "title": "Recipe Name",
  "meal_type": "Aftensmad",
  "portions": 4,
  "ingredients": [
    {
      "name": "Ingredient name",
      "quantity": 100,
      "unit": "g",
      "danish_alternative": "Alternative if needed"
    }
  ],
  "equipment": ["Pan", "Knife"],
  "instructions": ["Step 1", "Step 2"],
  "serving_suggestions": ["Serve with..."],
  "nutritional_summary": {
    "total_recipe": {
      "Energi_kcal": 1200,
      "Protein_g": 45,
      "Fedt_g": 30,
      "Heraf_Mættet_Fedt_g": 10,
      "Kulhydrater_g": 150,
      "Heraf_Sukkerarter_g": 20,
      "Salt_g": 2
    },
    "per_portion": { ... }
  }
}
```

## Project Structure

```
CRTR-refactor/
├── src/
│   └── crtr/
│       ├── __init__.py
│       ├── converter.py              # Main converter class
│       ├── convert_video_to_audio.py # Audio extraction
│       ├── transcribe_audio.py       # Whisper transcription
│       ├── generate_recipe_with_ai.py # Gemini AI integration
│       └── prompt.py                 # Recipe generation prompt
├── tests/
│   └── test_converter.py
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=crtr --cov-report=html
```

### Code Formatting

```bash
# Format code with black
black src/

# Check with flake8
flake8 src/
```

## Requirements

- `instaloader>=4.10.0` - Instagram content downloading
- `requests>=2.31.0` - HTTP requests
- `moviepy>=1.0.3` - Video processing
- `faster-whisper>=1.0.0` - Audio transcription
- `torch>=2.0.0` - Machine learning backend
- `google-genai>=0.2.0` - Google AI integration

## Limitations

- Instagram may rate-limit or block requests if used excessively
- Video downloads require the reel to be public
- Transcription quality depends on audio clarity
- AI-generated nutritional values are estimates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for audio transcription
- [Google Gemini](https://ai.google.dev/) for recipe generation
- [Instaloader](https://instaloader.github.io/) for Instagram integration

## Disclaimer

This tool is for educational and personal use only. Please respect Instagram's Terms of Service and content creators' rights when downloading content.
