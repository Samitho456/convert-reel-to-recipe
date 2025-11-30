"""Tests for the CRTR converter module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from crtr import ConvertReelToRecipe, ModelSize, GeminiModel


class TestConvertReelToRecipe:
    """Test suite for ConvertReelToRecipe class."""
    
    def test_initialization(self):
        """Test that the converter initializes correctly."""
        converter = ConvertReelToRecipe()
        assert converter.prompt_template is not None
        assert converter.prompt is None
        assert converter.transcript is None
        assert converter.description is None
        assert converter.shortcode is None
    
    def test_extract_shortcode_from_url(self):
        """Test extracting shortcode from various URL formats."""
        converter = ConvertReelToRecipe()
        
        # Test reel URL
        assert converter.extract_shortcode("https://www.instagram.com/reel/ABC123xyz/") == "ABC123xyz"
        
        # Test post URL
        assert converter.extract_shortcode("https://www.instagram.com/p/DEF456uvw/") == "DEF456uvw"
        
        # Test TV URL
        assert converter.extract_shortcode("https://www.instagram.com/tv/GHI789rst/") == "GHI789rst"
        
        # Test with query parameters
        assert converter.extract_shortcode("https://www.instagram.com/reel/JKL012mno/?utm_source=ig") == "JKL012mno"
        
        # Test plain shortcode
        assert converter.extract_shortcode("XYZ789abc") == "XYZ789abc"
    
    def test_build_prompt(self):
        """Test prompt building with description and transcript."""
        converter = ConvertReelToRecipe()
        
        description = "Delicious pasta recipe"
        transcript = "First, boil water. Then add pasta."
        
        prompt = converter.build_prompt(description, transcript)
        
        assert description in prompt
        assert transcript in prompt
        assert converter.prompt == prompt
    
    def test_get_prompt(self):
        """Test retrieving the formatted prompt."""
        converter = ConvertReelToRecipe()
        
        # Before building prompt
        assert converter.get_prompt() is None
        
        # After building prompt
        converter.build_prompt("Test description", "Test transcript")
        assert converter.get_prompt() is not None


class TestShortcodeExtraction:
    """Test suite specifically for shortcode extraction edge cases."""
    
    def test_empty_input(self):
        """Test with empty or None input."""
        converter = ConvertReelToRecipe()
        assert converter.extract_shortcode("") == ""
        assert converter.extract_shortcode(None) == ""
    
    def test_malformed_urls(self):
        """Test with malformed URLs."""
        converter = ConvertReelToRecipe()
        
        # Missing shortcode
        result = converter.extract_shortcode("https://www.instagram.com/")
        assert result is not None
        
        # Invalid format but contains instagram.com
        result = converter.extract_shortcode("https://instagram.com/someuser")
        assert result == "someuser"


class TestPromptFormatting:
    """Test suite for prompt formatting functionality."""
    
    def test_prompt_formatting_strips_whitespace(self):
        """Test that prompt formatting strips excess whitespace."""
        converter = ConvertReelToRecipe()
        
        description = "  Test description  "
        transcript = "  Test transcript  "
        
        prompt = converter.build_prompt(description, transcript)
        
        assert "Test description" in prompt
        assert "Test transcript" in prompt
        assert "  Test description  " not in prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
