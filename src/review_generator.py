"""
Generate HTML review reports for LEGO piece identifications.
"""
import json
import os
from typing import Dict, List, Optional
import base64
from pathlib import Path


def image_to_base64(image_path: str) -> str:
    """Convert image to base64 for embedding in HTML."""
    try:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"Warning: Could not encode image {image_path}: {e}")
        return ""


def generate_review_html(results: List[Dict], output_path: str, top_n: int = 3,
                         use_rebrickable: bool = True, api_key: Optional[str] = None) -> str:
    """
    Generate an HTML review page for identification results.

    Args:
        results: List of identification results
        output_path: Path to save the HTML file
        top_n: Number of top predictions to show per piece
        use_rebrickable: Whether to fetch images from Rebrickable API (default: True)
        api_key: Rebrickable API key (optional, will use env var if not provided)

    Returns:
        Path to the generated HTML file
    """

    # Fetch Rebrickable data if enabled
    part_images = {}
    if use_rebrickable:
        try:
            from rebrickable_client import RebrickableClient, get_api_key_from_file

            # Try to get API key from multiple sources
            key = api_key or get_api_key_from_file() or os.environ.get('REBRICKABLE_API_KEY')

            if key:
                print("Fetching part images from Rebrickable API...")
                client = RebrickableClient(api_key=key)

                # Collect all unique part numbers
                part_nums = set()
                for result in results:
                    items = result.get('items', [])
                    for item in items[:top_n]:
                        part_num = item.get('id')
                        if part_num:
                            part_nums.add(part_num)

                # Fetch all part info
                if part_nums:
                    part_data = client.get_parts_batch(list(part_nums))
                    # Store full part data (including variants if available)
                    for part_num, data in part_data.items():
                        if data and data.get('part_img_url'):
                            part_images[part_num] = {
                                'img_url': data['part_img_url'],
                                'name': data.get('name', ''),
                                'part_num': data.get('part_num', part_num),
                                'variants': data.get('variants', []),
                                'original_id': data.get('original_id', part_num)
                            }
                    print(f"✓ Fetched images for {len(part_images)} parts")
                else:
                    print("No parts to fetch from Rebrickable")
            else:
                print("⚠ Rebrickable API key not found - using placeholder images")
                print("  Set REBRICKABLE_API_KEY environment variable or create .rebrickable_key file")
                print("  Get your free API key at: https://rebrickable.com/api/")
        except ImportError:
            print("⚠ rebrickable_client module not found - using placeholder images")
        except Exception as e:
            print(f"⚠ Could not fetch Rebrickable data: {e}")
            print("  Continuing with placeholder images...")

    html_parts = ['''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LEGO Piece Identification Review</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin: 0 0 10px 0;
        }
        .stats {
            display: flex;
            gap: 30px;
            margin-top: 15px;
            font-size: 14px;
        }
        .stat-item {
            background: rgba(255,255,255,0.2);
            padding: 10px 20px;
            border-radius: 5px;
        }
        .piece-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .piece-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }
        .piece-number {
            background: #667eea;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }
        .piece-title {
            flex: 1;
        }
        .piece-content {
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 30px;
        }
        .captured-image {
            border: 2px solid #eee;
            border-radius: 8px;
            overflow: hidden;
        }
        .captured-image img {
            width: 100%;
            height: auto;
            display: block;
        }
        .captured-label {
            background: #667eea;
            color: white;
            padding: 8px;
            text-align: center;
            font-size: 12px;
            font-weight: bold;
        }
        .predictions {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .prediction {
            display: grid;
            grid-template-columns: 80px 1fr 2fr;
            gap: 15px;
            padding: 15px;
            border: 2px solid #eee;
            border-radius: 8px;
            align-items: start;
            transition: all 0.3s;
        }
        .images-container {
            display: flex;
            gap: 15px;
            align-items: start;
        }
        .image-group {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
        }
        .image-label {
            font-size: 10px;
            font-weight: 600;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .prediction:hover {
            border-color: #667eea;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
        }
        .prediction.top {
            border-color: #48bb78;
            background: #f0fff4;
        }
        .rank-badge {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
            color: white;
        }
        .rank-1 { background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); }
        .rank-2 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .rank-3 { background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%); }
        .rank-other { background: linear-gradient(135deg, #a0aec0 0%, #718096 100%); }

        .pred-image {
            width: 150px;
            height: 150px;
            object-fit: contain;
            border: 1px solid #eee;
            border-radius: 5px;
            background: white;
        }
        .pred-info {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .pred-id {
            font-size: 18px;
            font-weight: bold;
            color: #2d3748;
        }
        .pred-type {
            display: inline-block;
            padding: 4px 12px;
            background: #edf2f7;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            color: #4a5568;
            width: fit-content;
        }
        .confidence {
            font-size: 14px;
            color: #718096;
        }
        .confidence-bar {
            height: 6px;
            background: #edf2f7;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 5px;
        }
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #48bb78 0%, #38a169 100%);
            transition: width 0.3s;
        }
        .links {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        .link-btn {
            padding: 6px 12px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-size: 12px;
            transition: background 0.3s;
        }
        .link-btn:hover {
            background: #5568d3;
        }
        .no-results {
            padding: 30px;
            text-align: center;
            color: #a0aec0;
            font-style: italic;
        }
        .error-message {
            padding: 15px;
            background: #fed7d7;
            color: #c53030;
            border-radius: 8px;
            border: 1px solid #fc8181;
        }
        /* Interactive selection styles */
        .selection-controls {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 10px;
        }
        .select-checkbox {
            width: 20px;
            height: 20px;
            cursor: pointer;
        }
        .color-selector {
            padding: 6px 12px;
            border: 2px solid #e2e8f0;
            border-radius: 5px;
            background: white;
            font-size: 13px;
            cursor: pointer;
            min-width: 150px;
        }
        .color-selector:disabled {
            background: #f7fafc;
            cursor: not-allowed;
            opacity: 0.6;
        }
        .prediction.selected {
            border-color: #48bb78;
            background: #f0fff4;
            box-shadow: 0 0 0 3px rgba(72, 187, 120, 0.1);
        }
        .quantity-input {
            width: 60px;
            padding: 6px;
            border: 2px solid #e2e8f0;
            border-radius: 5px;
            font-size: 13px;
            text-align: center;
        }
        .action-bar {
            position: sticky;
            bottom: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 -4px 6px rgba(0,0,0,0.1);
            z-index: 1000;
        }
        .action-buttons {
            display: flex;
            gap: 15px;
        }
        .action-btn {
            padding: 12px 24px;
            background: white;
            color: #667eea;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .action-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        .action-btn.primary {
            background: #48bb78;
            color: white;
        }
        .action-btn.primary:hover {
            background: #38a169;
        }
        .selection-summary {
            color: white;
            font-size: 14px;
        }
        @media (max-width: 768px) {
            .piece-content {
                grid-template-columns: 1fr;
            }
            .prediction {
                grid-template-columns: 1fr;
                text-align: center;
            }
            .images-container {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 LEGO Piece Identification Review</h1>
        <div class="stats">
            <div class="stat-item">
                <strong>Total Pieces:</strong> ''' + str(len(results)) + '''
            </div>
            <div class="stat-item">
                <strong>Successfully Identified:</strong> ''' + str(sum(1 for r in results if r.get('items') and not r.get('error'))) + '''
            </div>
            <div class="stat-item">
                <strong>Failed:</strong> ''' + str(sum(1 for r in results if r.get('error') or not r.get('items'))) + '''
            </div>
        </div>
    </div>
''']

    # Generate piece sections
    for idx, result in enumerate(results):
        piece_index = result.get('piece_index', idx)
        image_path = result.get('image_path', '')

        # Encode image
        img_data = ""
        if os.path.exists(image_path):
            img_data = image_to_base64(image_path)

        html_parts.append(f'''
    <div class="piece-container">
        <div class="piece-header">
            <div class="piece-number">#{piece_index + 1}</div>
            <div class="piece-title">
                <h2 style="margin: 0;">Piece {piece_index + 1}</h2>
                <small style="color: #718096;">{os.path.basename(image_path)}</small>
            </div>
        </div>
        <div class="piece-content">
            <div class="captured-image">
                <div class="captured-label">YOUR PIECE</div>
''')

        if img_data:
            html_parts.append(f'                <img src="data:image/jpeg;base64,{img_data}" alt="Piece {piece_index + 1}">\n')
        else:
            html_parts.append('                <div style="padding: 50px; text-align: center; color: #a0aec0;">Image not available</div>\n')

        html_parts.append('            </div>\n            <div class="predictions">\n')

        # Handle errors
        if result.get('error'):
            html_parts.append(f'''
                <div class="error-message">
                    <strong>Error:</strong> {result['error']}
                </div>
''')
        elif not result.get('items'):
            html_parts.append('                <div class="no-results">No matching pieces found</div>\n')
        else:
            # Show predictions
            items = result.get('items', [])[:top_n]
            for rank, item in enumerate(items, 1):
                item_id = item.get('id', 'Unknown')
                item_type = item.get('type', 'part')
                score = item.get('score', 0)
                item_name = item.get('name', '')
                item_category = item.get('category', '')

                # Brickognize image from API results
                brickognize_img = item.get('img_url', '')
                if not brickognize_img:
                    brickognize_img = "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='150' height='150'><rect fill='%23eee' width='150' height='150'/><text x='50%' y='50%' text-anchor='middle' dy='.3em' fill='%23999' font-size='12'>No Image</text></svg>"

                rank_class = f"rank-{rank}" if rank <= 3 else "rank-other"
                top_class = "top" if rank == 1 else ""

                # Get Rebrickable image URL or use placeholder
                matched_part_num = item_id
                part_variants = []
                if item_id in part_images:
                    rebrickable_img_url = part_images[item_id]['img_url']
                    rebrickable_name = part_images[item_id].get('name', item_id)
                    matched_part_num = part_images[item_id].get('part_num', item_id)
                    part_variants = part_images[item_id].get('variants', [])
                else:
                    rebrickable_img_url = "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='150' height='150'><rect fill='%23eee' width='150' height='150'/><text x='50%' y='50%' text-anchor='middle' dy='.3em' fill='%23999' font-size='12'>No Image</text></svg>"
                    rebrickable_name = item_id

                # Use Rebrickable name if item name not available
                display_name = item_name if item_name else rebrickable_name

                # Links (use matched part number for Rebrickable, original for BrickLink)
                rebrickable_link = f"https://rebrickable.com/parts/{matched_part_num}/"
                bricklink_link = f"https://www.bricklink.com/v2/catalog/catalogitem.page?P={item_id}"

                # Auto-select if it's the only prediction or first with high confidence
                should_preselect = (len(items) == 1) or (rank == 1 and score > 0.7)
                selected_class = "selected" if should_preselect else ""
                checked_attr = "checked" if should_preselect else ""

                html_parts.append(f'''
                <div class="prediction {top_class} {selected_class}" data-piece-idx="{piece_index}" data-part-id="{matched_part_num}" data-rank="{rank}">
                    <div class="rank-badge {rank_class}">#{rank}</div>
                    <div class="images-container">
                        <div class="image-group">
                            <div class="image-label">Brickognize</div>
                            <img src="{brickognize_img}" alt="Brickognize: {item_id}" class="pred-image">
                        </div>
                        <div class="image-group">
                            <div class="image-label">Rebrickable</div>
                            <img src="{rebrickable_img_url}" alt="Rebrickable: {display_name}" class="pred-image" title="{display_name}">
                        </div>
                    </div>
                    <div class="pred-info">
                        <div class="pred-id">{matched_part_num}{f' <span style="font-size: 12px; color: #718096;">(BrickLink: {item_id})</span>' if matched_part_num != item_id else ''}</div>
                        {f'<div style="font-size: 14px; color: #4a5568; margin-bottom: 5px;"><strong>{display_name}</strong></div>' if display_name and display_name != matched_part_num else ''}
                        <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                            <span class="pred-type">{item_type}</span>
                            {f'<span class="pred-type" style="background: #e6fffa; color: #234e52;">{item_category}</span>' if item_category else ''}
                        </div>
                        <div class="confidence">
                            Confidence: <strong>{score * 100:.1f}%</strong>
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: {score * 100}%"></div>
                            </div>
                        </div>
                        <div class="links">
                            <a href="{rebrickable_link}" target="_blank" class="link-btn">Rebrickable</a>
                            <a href="{bricklink_link}" target="_blank" class="link-btn">BrickLink</a>
                        </div>
                        <div class="selection-controls">
                            <input type="checkbox"
                                   class="select-checkbox"
                                   id="select_{piece_index}_{rank}"
                                   data-piece-idx="{piece_index}"
                                   data-part-id="{matched_part_num}"
                                   {checked_attr}
                                   onchange="handleSelection(this)">
                            <label for="select_{piece_index}_{rank}" style="font-weight: 600; cursor: pointer;">
                                Select this piece
                            </label>
                        </div>
                        <div class="selection-controls" style="margin-top: 8px;">
                            <label style="font-weight: 600; min-width: 60px;">Color:</label>
                            <select class="color-selector"
                                    id="color_{piece_index}_{rank}"
                                    data-part-id="{matched_part_num}"
                                    {'' if should_preselect else 'disabled'}>
                                <option value="">Loading colors...</option>
                            </select>
                        </div>
                        <div class="selection-controls" style="margin-top: 8px;">
                            <label style="font-weight: 600; min-width: 60px;">Quantity:</label>
                            <input type="number"
                                   class="quantity-input"
                                   id="qty_{piece_index}_{rank}"
                                   min="1"
                                   value="1"
                                   {'' if should_preselect else 'disabled'}>
                        </div>
                    </div>
                </div>
''')

                # Add variant alternatives if they exist
                if part_variants:
                    html_parts.append(f'''
                <div style="margin-left: 95px; margin-top: 10px; padding-left: 15px; border-left: 3px solid #e2e8f0;">
                    <div style="font-size: 12px; font-weight: 600; color: #718096; margin-bottom: 10px;">
                        ⚡ ALTERNATIVE VARIANTS FOR {item_id}:
                    </div>
''')
                    for variant_idx, variant in enumerate(part_variants):
                        variant_part_num = variant.get('part_num', '')
                        variant_name = variant.get('name', '')
                        variant_img_url = variant.get('part_img_url', '')

                        if not variant_img_url:
                            variant_img_url = "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'><rect fill='%23eee' width='100' height='100'/><text x='50%' y='50%' text-anchor='middle' dy='.3em' fill='%23999' font-size='10'>No Image</text></svg>"

                        variant_rebrickable_link = f"https://rebrickable.com/parts/{variant_part_num}/"
                        variant_bricklink_link = f"https://www.bricklink.com/v2/catalog/catalogitem.page?P={variant_part_num}"

                        variant_rank_id = f"{rank}_var{variant_idx}"

                        html_parts.append(f'''
                    <div class="prediction" style="border-color: #cbd5e0; background: #f7fafc; margin-bottom: 10px;" data-piece-idx="{piece_index}" data-part-id="{variant_part_num}" data-rank="{variant_rank_id}">
                        <div style="width: 30px; height: 30px; border-radius: 50%; background: #cbd5e0; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #4a5568; font-weight: bold;">V{variant_idx + 1}</div>
                        <div class="images-container">
                            <div class="image-group">
                                <div class="image-label">Rebrickable</div>
                                <img src="{variant_img_url}" alt="Rebrickable: {variant_name}" class="pred-image" style="width: 100px; height: 100px;" title="{variant_name}">
                            </div>
                        </div>
                        <div class="pred-info">
                            <div class="pred-id" style="font-size: 16px;">{variant_part_num}</div>
                            {f'<div style="font-size: 13px; color: #4a5568; margin-bottom: 5px;"><strong>{variant_name}</strong></div>' if variant_name and variant_name != variant_part_num else ''}
                            <div class="links">
                                <a href="{variant_rebrickable_link}" target="_blank" class="link-btn" style="font-size: 11px; padding: 4px 10px;">Rebrickable</a>
                                <a href="{variant_bricklink_link}" target="_blank" class="link-btn" style="font-size: 11px; padding: 4px 10px;">BrickLink</a>
                            </div>
                            <div class="selection-controls" style="margin-top: 8px;">
                                <input type="checkbox"
                                       class="select-checkbox"
                                       id="select_{piece_index}_{variant_rank_id}"
                                       data-piece-idx="{piece_index}"
                                       data-part-id="{variant_part_num}"
                                       onchange="handleSelection(this)">
                                <label for="select_{piece_index}_{variant_rank_id}" style="font-weight: 600; cursor: pointer; font-size: 13px;">
                                    Select this variant
                                </label>
                            </div>
                            <div class="selection-controls" style="margin-top: 8px;">
                                <label style="font-weight: 600; min-width: 60px; font-size: 13px;">Color:</label>
                                <select class="color-selector"
                                        id="color_{piece_index}_{variant_rank_id}"
                                        data-part-id="{variant_part_num}"
                                        style="font-size: 12px;"
                                        disabled>
                                    <option value="">Loading colors...</option>
                                </select>
                            </div>
                            <div class="selection-controls" style="margin-top: 8px;">
                                <label style="font-weight: 600; min-width: 60px; font-size: 13px;">Quantity:</label>
                                <input type="number"
                                       class="quantity-input"
                                       id="qty_{piece_index}_{variant_rank_id}"
                                       min="1"
                                       value="1"
                                       style="font-size: 12px;"
                                       disabled>
                            </div>
                        </div>
                    </div>
''')

                    html_parts.append('                </div>\n')

        html_parts.append('            </div>\n        </div>\n    </div>\n')

    # Add action bar and JavaScript
    html_parts.append('''
    <div class="action-bar">
        <div class="selection-summary">
            <strong id="selection-count">0</strong> pieces selected
        </div>
        <div class="action-buttons">
            <button class="action-btn" onclick="saveSelections()">💾 Save Selections</button>
            <button class="action-btn" onclick="exportJSON()">📥 Export JSON</button>
            <button class="action-btn primary" onclick="importToRebrickable()" id="import-btn" disabled>
                🚀 Import to Rebrickable
            </button>
        </div>
    </div>

    <script>
        // Store API key and selections
        let rebrickableApiKey = localStorage.getItem('rebrickable_api_key') || '';
        let selections = JSON.parse(localStorage.getItem('lego_selections') || '{}');
        let colorCache = {};

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadSavedSelections();
            fetchAllColors();
            updateSelectionCount();
            checkApiKey();
        });

        function checkApiKey() {
            if (!rebrickableApiKey) {
                rebrickableApiKey = prompt('Enter your Rebrickable API key (get it from https://rebrickable.com/api/)\\nLeave blank to skip import feature:');
                if (rebrickableApiKey) {
                    localStorage.setItem('rebrickable_api_key', rebrickableApiKey);
                }
            }
            document.getElementById('import-btn').disabled = !rebrickableApiKey;
        }

        function handleSelection(checkbox) {
            const pieceIdx = checkbox.dataset.pieceIdx;
            const partId = checkbox.dataset.partId;
            const predictionDiv = checkbox.closest('.prediction');

            // Uncheck other checkboxes for this piece
            document.querySelectorAll(`input[data-piece-idx="${pieceIdx}"]`).forEach(cb => {
                if (cb !== checkbox) {
                    cb.checked = false;
                    cb.closest('.prediction').classList.remove('selected');
                    // Disable color/quantity for unselected
                    const rank = cb.id.split('_')[2];
                    document.getElementById(`color_${pieceIdx}_${rank}`).disabled = true;
                    document.getElementById(`qty_${pieceIdx}_${rank}`).disabled = true;
                }
            });

            // Update selected prediction
            if (checkbox.checked) {
                predictionDiv.classList.add('selected');
                const rank = checkbox.id.split('_')[2];
                document.getElementById(`color_${pieceIdx}_${rank}`).disabled = false;
                document.getElementById(`qty_${pieceIdx}_${rank}`).disabled = false;

                // Fetch colors for this part if not already cached
                fetchColorsForPart(partId);

                // Store selection
                selections[pieceIdx] = {
                    partId: partId,
                    color: document.getElementById(`color_${pieceIdx}_${rank}`).value,
                    quantity: parseInt(document.getElementById(`qty_${pieceIdx}_${rank}`).value) || 1
                };
            } else {
                predictionDiv.classList.remove('selected');
                delete selections[pieceIdx];
            }

            updateSelectionCount();
            localStorage.setItem('lego_selections', JSON.stringify(selections));
        }

        function updateSelectionCount() {
            const count = Object.keys(selections).length;
            document.getElementById('selection-count').textContent = count;
            document.getElementById('import-btn').disabled = count === 0 || !rebrickableApiKey;
        }

        async function fetchAllColors() {
            // Get all unique part IDs that are selected
            const partIds = new Set();
            document.querySelectorAll('.select-checkbox:checked').forEach(cb => {
                partIds.add(cb.dataset.partId);
            });

            for (const partId of partIds) {
                await fetchColorsForPart(partId);
            }
        }

        async function fetchColorsForPart(partId) {
            if (colorCache[partId] || !rebrickableApiKey) return;

            try {
                const response = await fetch(
                    `https://rebrickable.com/api/v3/lego/parts/${partId}/colors/`,
                    {
                        headers: {
                            'Authorization': `key ${rebrickableApiKey}`,
                            'Accept': 'application/json'
                        }
                    }
                );

                if (response.ok) {
                    const data = await response.json();
                    colorCache[partId] = data.results || [];
                    updateColorSelectors(partId);
                }
            } catch (error) {
                console.error(`Error fetching colors for ${partId}:`, error);
            }
        }

        function updateColorSelectors(partId) {
            const selectors = document.querySelectorAll(`select[data-part-id="${partId}"]`);
            const colors = colorCache[partId] || [];

            selectors.forEach(select => {
                select.innerHTML = '<option value="">Select color...</option>';
                colors.forEach(color => {
                    const option = document.createElement('option');
                    option.value = color.color_id;
                    option.textContent = `${color.color_name} (${color.num_sets} sets)`;
                    option.style.backgroundColor = `#${color.rgb || 'ffffff'}`;
                    select.appendChild(option);
                });

                // Restore saved selection if any
                const pieceIdx = select.id.split('_')[1];
                if (selections[pieceIdx] && selections[pieceIdx].color) {
                    select.value = selections[pieceIdx].color;
                }

                // Add change listener
                select.addEventListener('change', function() {
                    const rank = this.id.split('_')[2];
                    const checkbox = document.getElementById(`select_${pieceIdx}_${rank}`);
                    if (checkbox.checked) {
                        selections[pieceIdx].color = this.value;
                        localStorage.setItem('lego_selections', JSON.stringify(selections));
                    }
                });
            });
        }

        function loadSavedSelections() {
            for (const [pieceIdx, data] of Object.entries(selections)) {
                // Find and check the checkbox
                const partId = data.partId;
                const checkbox = document.querySelector(`input[data-piece-idx="${pieceIdx}"][data-part-id="${partId}"]`);
                if (checkbox) {
                    checkbox.checked = true;
                    handleSelection(checkbox);
                }
            }
        }

        function saveSelections() {
            const blob = new Blob([JSON.stringify(selections, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'lego_selections.json';
            a.click();
            alert('Selections saved to lego_selections.json');
        }

        function exportJSON() {
            const exportData = {
                timestamp: new Date().toISOString(),
                totalPieces: Object.keys(selections).length,
                pieces: []
            };

            for (const [pieceIdx, data] of Object.entries(selections)) {
                const qtyInput = document.querySelector(`input.quantity-input:not([disabled])`);
                exportData.pieces.push({
                    pieceIndex: parseInt(pieceIdx),
                    partId: data.partId,
                    colorId: data.color,
                    quantity: data.quantity || 1
                });
            }

            const blob = new Blob([JSON.stringify(exportData, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `lego_export_${Date.now()}.json`;
            a.click();
            alert(`Exported ${exportData.totalPieces} pieces to JSON`);
        }

        async function importToRebrickable() {
            if (!rebrickableApiKey) {
                alert('Please set your Rebrickable API key first');
                checkApiKey();
                return;
            }

            if (Object.keys(selections).length === 0) {
                alert('No pieces selected to import');
                return;
            }

            const userSetId = prompt('Enter your Rebrickable user set ID (or leave blank to skip)\\nFind it at: https://rebrickable.com/users/YOUR_USERNAME/sets/');

            if (!confirm(`Import ${Object.keys(selections).length} pieces to Rebrickable?`)) {
                return;
            }

            const importBtn = document.getElementById('import-btn');
            importBtn.disabled = true;
            importBtn.textContent = '⏳ Importing...';

            let successCount = 0;
            let failCount = 0;

            for (const [pieceIdx, data] of Object.entries(selections)) {
                if (!data.color) {
                    console.warn(`Skipping piece ${pieceIdx}: no color selected`);
                    failCount++;
                    continue;
                }

                try {
                    // Add part to user's collection
                    const payload = {
                        part_num: data.partId,
                        color_id: parseInt(data.color),
                        quantity: data.quantity || 1
                    };

                    const endpoint = userSetId
                        ? `https://rebrickable.com/api/v3/users/me/sets/${userSetId}/parts/`
                        : 'https://rebrickable.com/api/v3/users/me/parts/';

                    const response = await fetch(endpoint, {
                        method: 'POST',
                        headers: {
                            'Authorization': `key ${rebrickableApiKey}`,
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        },
                        body: JSON.stringify(payload)
                    });

                    if (response.ok) {
                        successCount++;
                    } else {
                        console.error(`Failed to import piece ${pieceIdx}:`, await response.text());
                        failCount++;
                    }

                    // Rate limiting
                    await new Promise(resolve => setTimeout(resolve, 200));

                } catch (error) {
                    console.error(`Error importing piece ${pieceIdx}:`, error);
                    failCount++;
                }
            }

            importBtn.disabled = false;
            importBtn.textContent = '🚀 Import to Rebrickable';

            alert(`Import complete!\\n✓ Success: ${successCount}\\n✗ Failed: ${failCount}`);
        }
    </script>
</body>
</html>''')

    # Write HTML file
    html_content = ''.join(html_parts)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path
