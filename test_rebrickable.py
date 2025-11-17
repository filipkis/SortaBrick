#!/usr/bin/env python3
"""
Quick test to verify Rebrickable API setup.
"""
import sys
import os

# Add src to path
sys.path.insert(0, 'src')

def test_api_key():
    """Test if API key is configured."""
    print("=" * 60)
    print("Testing Rebrickable API Setup")
    print("=" * 60)
    print()

    # Check for API key in various locations
    key_sources = []

    # Environment variable
    if os.environ.get('REBRICKABLE_API_KEY'):
        key_sources.append("✓ Environment variable (REBRICKABLE_API_KEY)")
    else:
        key_sources.append("✗ Environment variable (REBRICKABLE_API_KEY) - not set")

    # Key file
    if os.path.exists('.rebrickable_key'):
        key_sources.append("✓ Key file (.rebrickable_key)")
    else:
        key_sources.append("✗ Key file (.rebrickable_key) - not found")

    print("API Key Sources:")
    for source in key_sources:
        print(f"  {source}")
    print()

    # Try to initialize client
    try:
        from rebrickable_client import RebrickableClient
        print("Initializing Rebrickable API client...")

        try:
            client = RebrickableClient()
            print("✓ Client initialized successfully")
            print()

            # Test API call
            print("Testing API call (fetching part 3001 - 2x4 brick)...")
            result = client.get_part_info('3001')

            if result:
                print("✓ API call successful!")
                print()
                print("Part Details:")
                print(f"  Part Number: {result.get('part_num')}")
                print(f"  Name: {result.get('name')}")
                print(f"  Image URL: {result.get('part_img_url')}")
                print()
                print("=" * 60)
                print("✓ Rebrickable API is configured correctly!")
                print("=" * 60)
                return True
            else:
                print("✗ API call failed - part not found")
                print()
                print("This might indicate an API key issue.")
                return False

        except ValueError as e:
            print(f"✗ Error: {e}")
            print()
            print("To fix this:")
            print("1. Get your free API key from: https://rebrickable.com/api/")
            print("2. Set environment variable:")
            print("   export REBRICKABLE_API_KEY='your_key_here'")
            print("   OR")
            print("3. Create .rebrickable_key file:")
            print("   echo 'your_key_here' > .rebrickable_key")
            return False

    except ImportError:
        print("✗ Could not import rebrickable_client module")
        print("  Make sure you're in the legosorter directory")
        return False

    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_api_key()
    sys.exit(0 if success else 1)
