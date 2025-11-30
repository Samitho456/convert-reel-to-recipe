"""
Example usage of the CRTR package.

This script demonstrates how to use the ConvertReelToRecipe class
to convert Instagram cooking reels into structured recipes.
"""

from crtr import ConvertReelToRecipe, GeminiModel
import os

# Example Instagram reel URL
EXAMPLE_URL = "https://www.instagram.com/reel/ABC123xyz/"

# Get API key from environment variable
API_KEY = os.getenv("GOOGLE_AI_API_KEY")

if not API_KEY:
    print("⚠️  Please set GOOGLE_AI_API_KEY environment variable")
    print("Example: $env:GOOGLE_AI_API_KEY='your-key-here'")
    exit(1)


def main():
    """Main example function."""
    print("🍳 CRTR - Convert Reel To Recipe Example\n")
    
    # Initialize converter
    converter = ConvertReelToRecipe()
    
    # Convert reel to recipe
    print(f"Converting reel: {EXAMPLE_URL}")
    print("This may take a few minutes...\n")
    
    try:
        recipe = converter.convert_to_recipe_from_reel_url(
            reel_url=EXAMPLE_URL,
            ai_model=GeminiModel.GEMINI_2_0_FLASH.value,
            api_key=API_KEY
        )
        
        if recipe:
            print("\n✅ Recipe generated successfully!")
            print(f"\nRecipe JSON:\n{recipe}")
        else:
            print("\n❌ Failed to generate recipe")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
