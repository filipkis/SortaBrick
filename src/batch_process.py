#!/usr/bin/env python3
"""
Batch processing script for multiple LEGO images.
Processes all images in a directory.
"""
import argparse
import os
import sys
from pathlib import Path
from main import process_lego_image


def batch_process(input_dir: str, output_dir: str = "output",
                  min_area: int = 500, max_area: int = 100000,
                  category: str = "parts", visualize: bool = True):
    """
    Process all images in a directory.

    Args:
        input_dir: Directory containing input images
        output_dir: Base output directory
        min_area: Minimum piece area in pixels
        max_area: Maximum piece area in pixels
        category: Brickognize category
        visualize: Whether to create visualizations
    """
    # Supported image formats
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}

    # Find all images in input directory
    input_path = Path(input_dir)
    image_files = [
        f for f in input_path.iterdir()
        if f.is_file() and f.suffix.lower() in image_extensions
    ]

    if not image_files:
        print(f"No images found in {input_dir}")
        return

    print(f"Found {len(image_files)} images to process\n")

    results_summary = []

    for idx, image_file in enumerate(image_files, 1):
        print(f"\n{'=' * 80}")
        print(f"Processing image {idx}/{len(image_files)}: {image_file.name}")
        print(f"{'=' * 80}\n")

        # Create a subdirectory for each image's results
        image_output_dir = os.path.join(output_dir, image_file.stem)

        result = process_lego_image(
            input_image=str(image_file),
            output_dir=image_output_dir,
            min_area=min_area,
            max_area=max_area,
            category=category,
            visualize=visualize
        )

        results_summary.append({
            'image': image_file.name,
            'success': result.get('success', False),
            'pieces_detected': result.get('pieces_detected', 0)
        })

    # Print final summary
    print(f"\n\n{'=' * 80}")
    print("BATCH PROCESSING SUMMARY")
    print(f"{'=' * 80}\n")

    successful = sum(1 for r in results_summary if r['success'])
    total_pieces = sum(r['pieces_detected'] for r in results_summary)

    print(f"Total images processed: {len(results_summary)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results_summary) - successful}")
    print(f"Total pieces detected: {total_pieces}")

    print("\nDetails:")
    for r in results_summary:
        status = "✓" if r['success'] else "✗"
        print(f"  {status} {r['image']}: {r['pieces_detected']} pieces")

    print(f"\n{'=' * 80}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Batch process multiple LEGO images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  # Process all images in the input directory
  python batch_process.py ../input

  # Process with custom settings
  python batch_process.py ../input --output batch_results --min-area 300
        """
    )

    parser.add_argument("input_dir", help="Directory containing input images")
    parser.add_argument("--output", "-o", default="output",
                       help="Base output directory (default: output)")
    parser.add_argument("--min-area", type=int, default=500,
                       help="Minimum piece area in pixels (default: 500)")
    parser.add_argument("--max-area", type=int, default=100000,
                       help="Maximum piece area in pixels (default: 100000)")
    parser.add_argument("--category", "-c", choices=["parts", "sets", "figs"], default="parts",
                       help="Brickognize search category (default: parts)")
    parser.add_argument("--no-visualize", action="store_true",
                       help="Skip creating visualizations")

    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory not found: {args.input_dir}")
        sys.exit(1)

    batch_process(
        input_dir=args.input_dir,
        output_dir=args.output,
        min_area=args.min_area,
        max_area=args.max_area,
        category=args.category,
        visualize=not args.no_visualize
    )


if __name__ == "__main__":
    main()
