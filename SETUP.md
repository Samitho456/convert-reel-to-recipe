# CRTR Setup Guide

This guide will help you set up the CRTR package for development or production use.

## Quick Setup

### 1. Install in Development Mode

From the project root directory:

```powershell
# Install the package in editable mode with all dependencies
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### 2. Set Up API Key

Get your Google AI API key from: https://aistudio.google.com/app/apikey

Set it as an environment variable:

```powershell
# Windows PowerShell
$env:GOOGLE_AI_API_KEY = "your-api-key-here"

# Or permanently in PowerShell profile
Add-Content $PROFILE "`n`$env:GOOGLE_AI_API_KEY = 'your-api-key-here'"
```

### 3. Install FFmpeg

FFmpeg is required for video/audio processing:

```powershell
# Using Chocolatey (recommended)
choco install ffmpeg

# Verify installation
ffmpeg -version
```

## Running Tests

```powershell
# Run all tests
pytest

# Run with coverage report
pytest --cov=crtr --cov-report=html

# Run specific test file
pytest tests/test_converter.py -v
```

## Using the CLI

After installation, you can use the `crtr` command:

```powershell
# Basic usage
crtr "https://www.instagram.com/reel/ABC123xyz/" --api-key "your-key"

# Specify model
crtr "ABC123xyz" --api-key "your-key" --model gemini-2.0-flash

# Using environment variable for API key
$env:GOOGLE_AI_API_KEY = "your-key"
crtr "https://www.instagram.com/reel/ABC123xyz/" --api-key $env:GOOGLE_AI_API_KEY
```

## Using as a Library

```python
from crtr import ConvertReelToRecipe, GeminiModel

converter = ConvertReelToRecipe()
recipe = converter.convert_to_recipe_from_reel_url(
    reel_url="https://www.instagram.com/reel/ABC123xyz/",
    ai_model=GeminiModel.GEMINI_2_0_FLASH.value,
    api_key="your-google-ai-api-key"
)
print(recipe)
```

## Building the Package

```powershell
# Install build tools
pip install build

# Build the package
python -m build

# This creates:
# - dist/crtr-0.1.0.tar.gz (source distribution)
# - dist/crtr-0.1.0-py3-none-any.whl (wheel)
```

## Publishing to PyPI (Optional)

```powershell
# Install twine
pip install twine

# Upload to TestPyPI first (recommended)
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Code Quality Tools

```powershell
# Format code with black
black src/

# Check code style
flake8 src/

# Type checking
mypy src/
```

## Troubleshooting

### Import Errors

If you get import errors, make sure you installed in editable mode:

```powershell
pip install -e .
```

### FFmpeg Not Found

Ensure FFmpeg is in your PATH:

```powershell
ffmpeg -version
```

If not found, reinstall or add to PATH manually.

### CUDA/GPU Issues

For GPU acceleration with Whisper, ensure you have:

- NVIDIA GPU with CUDA support
- PyTorch with CUDA installed: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

The package will automatically fall back to CPU if CUDA is not available.

### Instagram Rate Limiting

If you encounter rate limiting:

- Wait a few minutes between requests
- Use a VPN or different network
- Consider using Instagram's official API for production use

## File Structure Reference

```
CRTR-refactor/
├── src/crtr/              # Main package source
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # Command-line interface
│   ├── converter.py       # Main converter class
│   ├── convert_video_to_audio.py
│   ├── transcribe_audio.py
│   ├── generate_recipe_with_ai.py
│   └── prompt.py          # AI prompt template
├── tests/                 # Test suite
│   ├── __init__.py
│   └── test_converter.py
├── pyproject.toml         # Package metadata
├── requirements.txt       # Dependencies
├── README.md             # Main documentation
├── LICENSE               # MIT License
├── CHANGELOG.md          # Version history
├── MANIFEST.in           # Package manifest
├── .gitignore            # Git ignore rules
└── example.py            # Usage example
```

## Next Steps

1. ✅ Install the package
2. ✅ Set up API keys
3. ✅ Install FFmpeg
4. ✅ Run the example script
5. ✅ Run tests to verify everything works
6. 🚀 Start converting reels to recipes!

## Support

For issues or questions:

- Check the README.md
- Review the example.py script
- Run tests to verify installation
- Open an issue on GitHub
