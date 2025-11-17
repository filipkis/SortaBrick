#!/usr/bin/env python3
"""
Identify LEGO pieces using Brickognize API only (no segmentation).
Use this when you already have individual piece images.
"""
import argparse
import os
import sys
from pathlib import Path
import json

from api_client import BrickognizeClient, format_results_summary


def identify_existing_pieces(input_dir: str, output_dir: str = "output/results",
                             category: str = "parts") -> dict:
    """
    Identify LEGO pieces from a directory of existing images.

    Args:
        input_dir: Directory containing individual piece images
        output_dir: Directory for output results
        category: Brickognize category ('parts', 'sets', or 'figs')

    Returns:
        Dictionary with processing results
    """
    print(f"\n{'=' * 80}")
    print(f"Identifying pieces from: {input_dir}")
    print(f"{'=' * 80}\n")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Find all images in input directory
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    input_path = Path(input_dir)

    image_files = [
        str(f) for f in input_path.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print(f"No images found in {input_dir}")
        return {"success": False, "error": "No images found"}

    # Sort files to have consistent ordering
    image_files.sort()

    print(f"Found {len(image_files)} images to identify\n")
    print("=" * 80)

    # Identify pieces using Brickognize API
    print(f"Identifying pieces using Brickognize API (category: {category})...")
    print("This may take a while...\n")

    client = BrickognizeClient(delay_between_requests=1.0)

    try:
        results = client.identify_multiple_pieces(image_files, category=category)
        print(f"\n✓ Identification complete")
    except Exception as e:
        print(f"✗ Error during identification: {e}")
        return {"success": False, "error": str(e)}

    # Save results
    print("\nSaving results...")

    # Generate output filename based on input directory name
    dir_name = Path(input_dir).name
    results_file = os.path.join(output_dir, f"{dir_name}_results.txt")
    json_file = os.path.join(output_dir, f"{dir_name}_results.json")

    # Save text summary
    summary = format_results_summary(results, results_file)
    print(f"✓ Results saved to: {results_file}")

    # Save JSON
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ JSON results saved to: {json_file}")

    # Print summary to console
    print("\n" + summary)

    return {
        "success": True,
        "pieces_identified": len(image_files),
        "results": results,
        "output_files": {
            "results_txt": results_file,
            "results_json": json_file
        }
    }


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Identify LEGO pieces using Brickognize API (no segmentation)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Identify pieces from a directory
  python identify_only.py output/pieces

  # Identify with custom output directory
  python identify_only.py my_pieces --output my_results

  # Search for minifigures instead of parts
  python identify_only.py minifig_images --category figs

  # Identify pieces you've already manually cropped
  python identify_only.py manually_cropped_pieces
        """
    )

    parser.add_argument("input_dir", help="Directory containing individual piece images")
    parser.add_argument("--output", "-o", default="output/results",
                       help="Output directory for results (default: output/results)")
    parser.add_argument("--category", "-c", choices=["parts", "sets", "figs"], default="parts",
                       help="Brickognize search category (default: parts)")

    args = parser.parse_args()

    # Validate input directory
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory not found: {args.input_dir}")
        sys.exit(1)

    # Process the images
    result = identify_existing_pieces(
        input_dir=args.input_dir,
        output_dir=args.output,
        category=args.category
    )

    if result["success"]:
        print(f"\n{'=' * 80}")
        print("✓ Identification complete!")
        print(f"{'=' * 80}\n")
        sys.exit(0)
    else:
        print(f"\n{'=' * 80}")
        print(f"✗ Identification failed: {result.get('error', 'Unknown error')}")
        print(f"{'=' * 80}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
