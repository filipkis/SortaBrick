#!/usr/bin/env python3
"""
Generate a review HTML from existing JSON results.
Useful for regenerating reviews or viewing old results.
"""
import argparse
import json
import os
import sys
from pathlib import Path

from review_generator import generate_review_html


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate HTML review from existing JSON results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate review from JSON results
  python generate_review.py output/results/my_pieces_results.json

  # Specify custom output location
  python generate_review.py results.json --output my_review.html

  # Show more predictions per piece
  python generate_review.py results.json --top-n 5
        """
    )

    parser.add_argument("json_file", help="Path to JSON results file")
    parser.add_argument("--output", "-o", help="Output HTML file (default: same dir as JSON)")
    parser.add_argument("--top-n", type=int, default=3,
                       help="Number of top predictions to show (default: 3)")
    parser.add_argument("--no-rebrickable", action="store_true",
                       help="Don't fetch images from Rebrickable API (use placeholders)")
    parser.add_argument("--api-key", help="Rebrickable API key (optional, uses env var if not provided)")

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.json_file):
        print(f"Error: JSON file not found: {args.json_file}")
        sys.exit(1)

    # Load results
    print(f"Loading results from: {args.json_file}")
    try:
        with open(args.json_file, 'r') as f:
            results = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)

    # Determine output path
    if args.output:
        output_file = args.output
    else:
        # Same directory as JSON, replace extension
        output_file = Path(args.json_file).with_suffix('.html')

    # Generate review
    print(f"Generating review page...")
    try:
        generate_review_html(
            results,
            str(output_file),
            top_n=args.top_n,
            use_rebrickable=not args.no_rebrickable,
            api_key=args.api_key
        )
        print(f"✓ Review page saved to: {output_file}")
        print(f"\nOpen the file in your browser to review the identifications")
    except Exception as e:
        print(f"✗ Error generating review: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
