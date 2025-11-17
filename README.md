# LEGO Sorter

An automated tool for identifying LEGO pieces from photos using computer vision and the Brickognize API.

## Features

- **Automatic Segmentation**: Detects and extracts individual LEGO pieces from a single photo containing multiple pieces
- **API Integration**: Uses the Brickognize API to identify each piece
- **Batch Processing**: Processes all detected pieces automatically
- **Visual Feedback**: Creates annotated images showing detected pieces
- **Detailed Results**: Exports results in both human-readable text and JSON formats
- **Rebrickable Integration**: Get piece IDs that can be used directly on Rebrickable

## How It Works

1. **Image Segmentation**: Uses OpenCV to detect individual LEGO pieces in your photo
2. **Piece Extraction**: Crops each piece into a separate image
3. **Identification**: Sends each piece to the Brickognize API for identification
4. **Results Export**: Saves all results with confidence scores and piece details

## Prerequisites

- Python 3.8 or higher
- A photo of your LEGO pieces (pieces should not be touching each other)
- Internet connection (for Brickognize API)

## Installation

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

1. Place your LEGO photo in the `input` directory

2. Run the script:
```bash
cd src
python main.py ../input/your_lego_photo.jpg
```

3. Results will be saved in the `output` directory:
   - `output/pieces/`: Individual piece images
   - `output/results/`: Identification results (text and JSON)
   - `output/results/detected_pieces.jpg`: Visualization with bounding boxes

### Advanced Usage

```bash
# Custom output directory
python main.py input/lego_pieces.jpg --output my_results

# Adjust detection sensitivity for smaller pieces
python main.py input/lego_pieces.jpg --min-area 200

# Search for minifigures instead of parts
python main.py input/minifigs.jpg --category figs

# Search for sets
python main.py input/sets.jpg --category sets

# Skip visualization to save time
python main.py input/lego_pieces.jpg --no-visualize
```

### Two-Step Workflow: Segment First, Identify Later

If you want to separate segmentation from API identification:

```bash
# Step 1: Only segment the image (no API calls)
python main.py ../input/lego_pieces.jpg --segment-only

# Step 2: Later, identify the segmented pieces
python identify_only.py ../output/pieces
```

This is useful if you want to:
- Review segmented pieces before sending to API
- Process multiple batches of segmentation before identification
- Avoid API calls during testing

### Identify Pre-Existing Individual Piece Images

If you already have individual piece images (manually cropped or from previous segmentation):

```bash
# Identify pieces from any directory
python identify_only.py path/to/piece/images

# With custom output location
python identify_only.py my_pieces --output results --category parts
```

### Batch Processing Multiple Images

To process multiple images at once:

```bash
# Process all images in a directory
python batch_process.py ../input

# With custom settings
python batch_process.py ../input --output batch_results --min-area 300
```

Each image will be processed separately, and results will be organized in subdirectories.

### Command Line Options

**main.py** - Full workflow (segment + identify):
- `input_image`: Path to your input image (required)
- `--output, -o`: Output directory (default: `output`)
- `--min-area`: Minimum piece area in pixels (default: 500)
- `--max-area`: Maximum piece area in pixels (default: 100000)
- `--category, -c`: Search category - `parts`, `sets`, or `figs` (default: `parts`)
- `--no-visualize`: Skip creating the visualization image
- `--segment-only`: Only segment, skip API identification

**identify_only.py** - API identification only:
- `input_dir`: Directory containing individual piece images (required)
- `--output, -o`: Output directory for results (default: `output/results`)
- `--category, -c`: Search category - `parts`, `sets`, or `figs` (default: `parts`)

## Tips for Best Results

### Photography Tips

1. **Lighting**: Use even, bright lighting to avoid shadows
2. **Background**: Use a plain, contrasting background (white or light-colored works best)
3. **Spacing**: Make sure pieces don't touch each other
4. **Orientation**: Place pieces flat on the surface
5. **Focus**: Ensure the image is sharp and in focus
6. **Resolution**: Higher resolution images work better (but not required)

### Troubleshooting

**Too many/few pieces detected?**
- Adjust `--min-area` and `--max-area` parameters
- Check the visualization image to see what's being detected
- Improve lighting and background contrast

**Poor identification results?**
- Try photographing pieces individually or in smaller groups
- Ensure pieces are clean and visible
- Use better lighting
- Try different angles for oddly-shaped pieces

**API errors?**
- Check your internet connection
- The script includes rate limiting (1 second between requests)
- Brickognize API is free but may have usage limits

## Project Structure

```
legosorter/
├── src/
│   ├── main.py           # Main workflow (segment + identify)
│   ├── identify_only.py  # API identification only (skip segmentation)
│   ├── batch_process.py  # Batch processing (multiple images)
│   ├── segmentation.py   # Image segmentation module
│   └── api_client.py     # Brickognize API client
├── input/                # Place your input images here
├── output/               # Output directory (created automatically)
│   ├── pieces/          # Extracted individual piece images
│   └── results/         # Identification results
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Output Format

### Text Results

The text file contains a formatted summary with:
- Total pieces processed
- Success/failure count
- Top 5 predictions for each piece with confidence scores

### JSON Results

The JSON file contains complete data for programmatic processing:
- All predictions for each piece
- Image paths
- Piece indices
- Confidence scores
- Item IDs compatible with Rebrickable

## Using Results with Rebrickable

The piece IDs returned by Brickognize can be used directly on Rebrickable.com to:
- Add pieces to your collection
- Find which sets contain specific pieces
- Calculate set completion percentages
- Create custom part lists

## API Information

This tool uses the [Brickognize API](https://brickognize.com/), which is currently free to use. The API can identify:
- Individual LEGO parts/pieces
- LEGO sets
- Minifigures

The script includes a 1-second delay between API requests to be respectful of the service.

## License

This project is provided as-is for personal use. Brickognize is a separate service with its own terms of use.

## Acknowledgments

- [Brickognize](https://brickognize.com/) for providing the LEGO piece identification API
- [Rebrickable](https://rebrickable.com/) for LEGO database and cataloging tools
- OpenCV community for the computer vision tools
