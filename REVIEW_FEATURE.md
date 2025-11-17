# Review Feature

## Overview

The review feature generates a beautiful, interactive HTML page that lets you visually confirm LEGO piece identifications before adding them to your collection.

## What You Get

### Visual Comparison
- **Your piece**: The actual photo you captured
- **BrickLink images**: Official reference images for each identified piece
- Side-by-side layout for easy comparison

### Identification Details
- Top 3 predictions per piece (or configure with `--top-n`)
- Confidence scores (percentage)
- Visual progress bars showing confidence
- Color-coded rankings:
  - 🥇 #1 prediction (green highlight)
  - 🥈 #2 prediction (purple badge)
  - 🥉 #3 prediction (orange badge)

### Direct Links
- Click through to **Rebrickable** for detailed part info
- Click through to **BrickLink** to check availability and pricing
- No need to manually search for part numbers

### Convenience
- Works offline (images embedded in HTML)
- Responsive design (works on phone, tablet, desktop)
- Professional styling with gradient colors
- Easy to navigate and review

## How to Use

### Automatic Generation

The review page is **automatically created** every time you run identification:

```bash
# Full workflow - review page generated automatically
python main.py input/lego_pieces.jpg

# Identify only - review page generated automatically
python identify_only.py output/pieces
```

The HTML file will be saved in the results directory:
- `output/results/[image_name]_review.html`

### Manual Generation

Generate or regenerate review from existing JSON results:

```bash
# Generate from JSON results
python generate_review.py output/results/my_pieces_results.json

# Custom output location
python generate_review.py results.json --output my_review.html

# Show top 5 predictions instead of 3
python generate_review.py results.json --top-n 5
```

## Opening the Review

Simply double-click the HTML file or open it in your browser:

```bash
# macOS
open output/results/my_pieces_review.html

# Linux
xdg-open output/results/my_pieces_review.html

# Windows
start output/results/my_pieces_review.html
```

## Review Page Layout

```
┌─────────────────────────────────────────────────────┐
│  🔍 LEGO Piece Identification Review                │
│  Total: 15 | Success: 14 | Failed: 1                │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  #1 Piece 1                          piece_001.jpg  │
├──────────────┬──────────────────────────────────────┤
│              │  #1  [BrickLink Image]  3001         │
│  YOUR PIECE  │      part                            │
│  [Your      │      Confidence: 95.3%  ████████████ │
│   Photo]     │      [Rebrickable] [BrickLink]       │
│              │                                       │
│              │  #2  [BrickLink Image]  3002         │
│              │      part                            │
│              │      Confidence: 78.2%  ████████     │
│              │      [Rebrickable] [BrickLink]       │
│              │                                       │
│              │  #3  [BrickLink Image]  3003         │
│              │      part                            │
│              │      Confidence: 45.1%  █████        │
│              │      [Rebrickable] [BrickLink]       │
└──────────────┴──────────────────────────────────────┘

[Repeat for each piece...]
```

## Use Cases

1. **Quick Verification**: Glance through all pieces and verify identifications visually
2. **Uncertain Pieces**: Compare multiple predictions when confidence is low
3. **Inventory Management**: Click through to Rebrickable to add confirmed pieces
4. **Documentation**: Save HTML files as records of your sorting sessions
5. **Sharing**: Email or share HTML files with others (all images embedded)

## Tips

- **Top prediction is usually correct** if confidence > 80%
- **Check alternates** if the first result doesn't look quite right
- **Use Rebrickable links** to see what sets contain the piece
- **Save review files** for your records before sorting another batch
- **Open on phone/tablet** while physically sorting pieces

## Technical Details

- Images are base64-encoded and embedded in HTML
- No external dependencies (works offline)
- Uses BrickLink image URLs for reference images
- Fallback to "No Image" placeholder if BrickLink image not available
- Responsive CSS grid layout
- Progressive enhancement with hover effects
