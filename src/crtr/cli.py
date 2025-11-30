"""Command-line interface for CRTR."""

import sys
import argparse
from . import ConvertReelToRecipe, GeminiModel


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert Instagram cooking reels to structured recipes"
    )
    parser.add_argument(
        "url",
        help="Instagram reel URL or shortcode"
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="Google AI API key"
    )
    parser.add_argument(
        "--model",
        default=GeminiModel.GEMINI_2_0_FLASH.value,
        choices=[m.value for m in GeminiModel],
        help="AI model to use (default: gemini-2.0-flash)"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: <shortcode>.json)"
    )
    
    args = parser.parse_args()
    
    try:
        converter = ConvertReelToRecipe()
        print(f"Converting reel: {args.url}")
        
        recipe = converter.convert_to_recipe_from_reel_url(
            reel_url=args.url,
            ai_model=args.model,
            api_key=args.api_key
        )
        
        if recipe:
            print("\n✅ Recipe generated successfully!")
            if not args.output:
                print(f"Saved to: {converter.shortcode}.json")
            else:
                print(f"Saved to: {args.output}")
        else:
            print("\n❌ Failed to generate recipe")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
