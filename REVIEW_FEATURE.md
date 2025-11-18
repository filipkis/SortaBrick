# Interactive Review Feature

## Overview

The review feature generates a beautiful, fully interactive HTML page that lets you visually confirm LEGO piece identifications, select colors, and import directly to your Rebrickable collection - all from your browser!

## What You Get

### Visual Comparison
- **Your piece**: The actual photo you captured
- **Brickognize image**: Image from Brickognize API results
- **Rebrickable image**: Official reference image from Rebrickable database
- Side-by-side layout for easy comparison

### Identification Details
- Top 3 predictions per piece (or configure with `--top-n`)
- **Part name** from Rebrickable database
- **Category** information for each part
- **Part ID** (compatible with Rebrickable)
- **Type** (part, set, or minifig)
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

### Interactive Features (NEW!)
- ✅ **Select correct identification** - checkboxes to confirm which prediction is right
- 🎨 **Color picker** - dropdown with all available colors from Rebrickable
- 🔢 **Quantity input** - specify how many of each piece you have
- 💾 **Auto-save** - selections saved to browser localStorage
- 📤 **Export** - save selections as JSON
- 🚀 **Direct import** - add parts to Rebrickable with one click

### Convenience
- Auto-selects first prediction if only one option or high confidence (>70%)
- Works with Rebrickable API to fetch real-time color availability
- Color options show number of sets each color appears in
- Selections persist between sessions (localStorage)
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

## Interactive Workflow

### 1. Initial Load
- Review page opens in your browser
- If you have pieces with only one prediction or high confidence (>70%), they're auto-selected
- You'll be prompted for your Rebrickable API key (one-time setup)

### 2. Review and Select
For each piece:
- **Check the prediction** - Look at both Brickognize and Rebrickable images
- **Select correct match** - Click checkbox next to the correct identification
  - Only one prediction per piece can be selected
  - Uncheck to deselect if none match
- **Choose color** - Dropdown automatically loads available colors from Rebrickable
  - Colors show as "(color name) (X sets)" where X = number of sets with that color
  - Color swatch displayed for visual reference
- **Set quantity** - Enter how many pieces you have (default: 1)

### 3. Actions
Bottom action bar shows:
- **Selection count** - "X pieces selected"
- **💾 Save Selections** - Download your selections as JSON (backup)
- **📥 Export JSON** - Export formatted data for external tools
- **🚀 Import to Rebrickable** - Push selected parts directly to your Rebrickable account

### 4. Import to Rebrickable
When you click "Import to Rebrickable":
1. Optionally enter a user set ID (to add parts to a specific set)
2. Confirm import
3. Watch progress as parts are added
4. See success/failure summary

**Requirements:**
- Rebrickable API key (free from https://rebrickable.com/api/)
- Color must be selected for each part
- Internet connection

## Review Page Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  🔍 LEGO Piece Identification Review                             │
│  Total: 15 | Success: 14 | Failed: 1                             │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│  #1 Piece 1                                      piece_001.jpg   │
├──────────────┬───────────────────────────────────────────────────┤
│              │  #1  [Brickognize] [Rebrickable]  3001            │
│  YOUR PIECE  │      Brick 2 x 4                                  │
│  [Your      │      part | Bricks                                │
│   Photo]     │      Confidence: 95.3%  ████████████              │
│              │      [Rebrickable] [BrickLink]                    │
│              │                                                    │
│              │  #2  [Brickognize] [Rebrickable]  3002            │
│              │      Brick 2 x 3                                  │
│              │      part | Bricks                                │
│              │      Confidence: 78.2%  ████████                  │
│              │      [Rebrickable] [BrickLink]                    │
│              │                                                    │
│              │  #3  [Brickognize] [Rebrickable]  3003            │
│              │      Brick 2 x 2                                  │
│              │      part | Bricks                                │
│              │      Confidence: 45.1%  █████                     │
│              │      [Rebrickable] [BrickLink]                    │
└──────────────┴───────────────────────────────────────────────────┘

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
