#!/usr/bin/env python3
"""
Main workflow script for LEGO piece identification.
Takes an image with multiple LEGO pieces, segments them, and identifies each piece.
"""
import argparse
import os
import sys
from pathlib import Path

from segmentation import LegoSegmenter
from api_client import BrickognizeClient, format_results_summary
from review_generator import generate_review_html


def process_lego_image(input_image: str, output_dir: str = "output",
                       min_area: int = 500, max_area: int = 100000,
                       category: str = "parts", visualize: bool = True,
                       segment_only: bool = False) -> dict:
    """
    Process a LEGO image: segment pieces and identify them.

    Args:
        input_image: Path to input image containing multiple LEGO pieces
        output_dir: Directory for output files
        min_area: Minimum piece area in pixels
        max_area: Maximum piece area in pixels
        category: Brickognize category ('parts', 'sets', or 'figs')
        visualize: Whether to create a visualization of detected pieces
        segment_only: If True, only segment the image without calling API

    Returns:
        Dictionary with processing results
    """
    print(f"\n{'=' * 80}")
    print(f"Processing: {input_image}")
    print(f"{'=' * 80}\n")

    # Create output directories
    pieces_dir = os.path.join(output_dir, "pieces")
    results_dir = os.path.join(output_dir, "results")
    os.makedirs(pieces_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    # Step 1: Segment the image
    print("Step 1: Segmenting image to detect individual pieces...")
    segmenter = LegoSegmenter(min_area=min_area, max_area=max_area, padding=10)

    try:
        image, bounding_boxes = segmenter.detect_pieces(input_image)
        print(f"✓ Detected {len(bounding_boxes)} pieces")
    except Exception as e:
        print(f"✗ Error during segmentation: {e}")
        return {"success": False, "error": str(e)}

    # Create visualization if requested
    if visualize:
        vis_path = os.path.join(results_dir, "detected_pieces.jpg")
        segmenter.visualize_detection(image, bounding_boxes, vis_path)
        print(f"✓ Visualization saved to: {vis_path}")

    # Step 2: Extract individual pieces
    print("\nStep 2: Extracting individual pieces...")
    base_name = Path(input_image).stem
    try:
        piece_paths = segmenter.extract_pieces(image, bounding_boxes, pieces_dir, base_name)
        print(f"✓ Extracted {len(piece_paths)} pieces to: {pieces_dir}")
    except Exception as e:
        print(f"✗ Error during extraction: {e}")
        return {"success": False, "error": str(e)}

    # If segment_only is True, skip API call
    if segment_only:
        print(f"\n{'=' * 80}")
        print("Segmentation complete! Skipping API identification.")
        print(f"To identify these pieces later, run:")
        print(f"  python identify_only.py {pieces_dir}")
        print(f"{'=' * 80}\n")

        return {
            "success": True,
            "pieces_detected": len(bounding_boxes),
            "pieces_extracted": len(piece_paths),
            "output_files": {
                "pieces_dir": pieces_dir,
                "visualization": vis_path if visualize else None
            }
        }

    # Step 3: Identify pieces using Brickognize API
    print(f"\nStep 3: Identifying pieces using Brickognize API (category: {category})...")
    print("This may take a while...\n")

    client = BrickognizeClient(delay_between_requests=1.0)

    try:
        results = client.identify_multiple_pieces(piece_paths, category=category)
        print(f"\n✓ Identification complete")
    except Exception as e:
        print(f"✗ Error during identification: {e}")
        return {"success": False, "error": str(e)}

    # Step 4: Save results
    print("\nStep 4: Saving results...")
    results_file = os.path.join(results_dir, f"{base_name}_results.txt")
    summary = format_results_summary(results, results_file)
    print(f"✓ Results saved to: {results_file}")

    # Also save as JSON for easier processing
    import json
    json_file = os.path.join(results_dir, f"{base_name}_results.json")
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ JSON results saved to: {json_file}")

    # Generate HTML review
    print("\nStep 5: Generating review page...")
    review_file = os.path.join(results_dir, f"{base_name}_review.html")
    try:
        generate_review_html(results, review_file, top_n=3)
        print(f"✓ Review page saved to: {review_file}")
        print(f"  Open in browser to review identifications")
    except Exception as e:
        print(f"⚠ Warning: Could not generate review page: {e}")
        review_file = None

    # Print summary to console
    print("\n" + summary)

    return {
        "success": True,
        "pieces_detected": len(bounding_boxes),
        "pieces_extracted": len(piece_paths),
        "results": results,
        "output_files": {
            "pieces_dir": pieces_dir,
            "results_txt": results_file,
            "results_json": json_file,
            "review_html": review_file,
            "visualization": vis_path if visualize else None
        }
    }


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Segment and identify LEGO pieces from an image",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single image
  python main.py input/lego_pieces.jpg

  # Process with custom output directory
  python main.py input/lego_pieces.jpg --output my_results

  # Adjust sensitivity for smaller pieces
  python main.py input/lego_pieces.jpg --min-area 200

  # Search for minifigures instead of parts
  python main.py input/minifigs.jpg --category figs

  # Only segment, don't call API (identify later)
  python main.py input/lego_pieces.jpg --segment-only
        """
    )

    parser.add_argument("input_image", help="Path to input image containing LEGO pieces")
    parser.add_argument("--output", "-o", default="output",
                       help="Output directory for results (default: output)")
    parser.add_argument("--min-area", type=int, default=500,
                       help="Minimum piece area in pixels (default: 500)")
    parser.add_argument("--max-area", type=int, default=100000,
                       help="Maximum piece area in pixels (default: 100000)")
    parser.add_argument("--category", "-c", choices=["parts", "sets", "figs"], default="parts",
                       help="Brickognize search category (default: parts)")
    parser.add_argument("--no-visualize", action="store_true",
                       help="Skip creating visualization of detected pieces")
    parser.add_argument("--segment-only", action="store_true",
                       help="Only segment pieces, skip API identification")

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input_image):
        print(f"Error: Input file not found: {args.input_image}")
        sys.exit(1)

    # Process the image
    result = process_lego_image(
        input_image=args.input_image,
        output_dir=args.output,
        min_area=args.min_area,
        max_area=args.max_area,
        category=args.category,
        visualize=not args.no_visualize,
        segment_only=args.segment_only
    )

    if result["success"]:
        print(f"\n{'=' * 80}")
        print("✓ Processing complete!")
        print(f"{'=' * 80}\n")
        sys.exit(0)
    else:
        print(f"\n{'=' * 80}")
        print(f"✗ Processing failed: {result.get('error', 'Unknown error')}")
        print(f"{'=' * 80}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
