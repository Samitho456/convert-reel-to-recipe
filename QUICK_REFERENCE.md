# Quick Reference - CRTR Package

## Installation

```powershell
pip install -e .                 # Development mode
pip install -e ".[dev]"          # With dev dependencies
```

## Import & Use

```python
from crtr import ConvertReelToRecipe, GeminiModel

converter = ConvertReelToRecipe()
recipe = converter.convert_to_recipe_from_reel_url(
    reel_url="https://www.instagram.com/reel/ABC123xyz/",
    ai_model=GeminiModel.GEMINI_2_0_FLASH.value,
    api_key="your-api-key"
)
```

## CLI Usage

```powershell
crtr "https://www.instagram.com/reel/ABC/" --api-key "your-key"
```

## Run Tests

```powershell
pytest                                    # Run all tests
pytest --cov=crtr                        # With coverage
pytest tests/test_converter.py -v       # Specific file
```

## Build & Publish

```powershell
python -m build                          # Build package
twine upload dist/*                      # Upload to PyPI
```

## File Locations

- **Source code**: `src/crtr/`
- **Tests**: `tests/`
- **Config**: `pyproject.toml`
- **Docs**: `README.md`, `SETUP.md`

## Next Actions

1. ✏️ Update author info in `pyproject.toml`
2. 🧪 Run tests: `pytest`
3. 🎨 Format code: `black src/`
4. 📦 Build: `python -m build`
5. 🚀 Publish to PyPI (optional)
