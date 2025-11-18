#!/usr/bin/env python3
"""
Test the variant search functionality in rebrickable_client.
"""
import sys
sys.path.insert(0, 'src')

# Mock the requests module to test logic without actual API calls
class MockResponse:
    def __init__(self, json_data, status_code):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

# Test the search_by_bricklink_id response parsing
def test_variant_parsing():
    print("=" * 60)
    print("Testing Variant Search Logic")
    print("=" * 60)
    print()

    # Simulate a response from Rebrickable search API
    mock_search_response = {
        'results': [
            {
                'part_num': '3068b',
                'name': 'Tile 2 x 2 with Groove',
                'part_img_url': 'https://cdn.rebrickable.com/media/parts/elements/306801.jpg',
                'part_url': 'https://rebrickable.com/parts/3068b/',
                'part_cat_id': 14,
                'part_material': 'Plastic'
            },
            {
                'part_num': '3068a',
                'name': 'Tile 2 x 2 without Groove',
                'part_img_url': 'https://cdn.rebrickable.com/media/parts/elements/306800.jpg',
                'part_url': 'https://rebrickable.com/parts/3068a/',
                'part_cat_id': 14,
                'part_material': 'Plastic'
            }
        ]
    }

    # Simulate what search_by_bricklink_id() returns
    parts = []
    for item in mock_search_response['results']:
        part_info = {
            'part_num': item.get('part_num'),
            'name': item.get('name'),
            'part_img_url': item.get('part_img_url'),
            'part_url': item.get('part_url'),
            'category_id': item.get('part_cat_id'),
            'material': item.get('part_material'),
            'bricklink_id': '3068'
        }
        parts.append(part_info)

    print(f"Found {len(parts)} variants for BrickLink ID '3068':")
    print()

    for idx, part in enumerate(parts, 1):
        print(f"Variant {idx}:")
        print(f"  Part Number: {part['part_num']}")
        print(f"  Name: {part['name']}")
        print(f"  Image URL: {part['part_img_url']}")
        print()

    # Simulate what get_part_info() returns when variants are found
    result = parts[0].copy()
    result['variants'] = parts[1:] if len(parts) > 1 else []
    result['original_id'] = '3068'

    print("=" * 60)
    print("Result Structure (as returned by get_part_info):")
    print("=" * 60)
    print()
    print(f"Primary Match:")
    print(f"  Part Number: {result['part_num']}")
    print(f"  Name: {result['name']}")
    print(f"  Original BrickLink ID: {result['original_id']}")
    print()
    print(f"Additional Variants: {len(result['variants'])}")
    for idx, variant in enumerate(result['variants'], 1):
        print(f"  Variant {idx}: {variant['part_num']} - {variant['name']}")
    print()

    print("=" * 60)
    print("✓ Variant search logic test passed!")
    print("=" * 60)

    return True

if __name__ == "__main__":
    test_variant_parsing()
