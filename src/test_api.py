#!/usr/bin/env python3
"""
Test script to debug Brickognize API connection.
"""
import requests
import sys
import os


def test_api_connection():
    """Test basic API connectivity."""
    print("Testing Brickognize API connection...\n")

    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get("https://api.brickognize.com/health/", timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}\n")
    except Exception as e:
        print(f"   Error: {e}\n")

    # Test 2: Check if we have a test image
    print("2. Checking for test image...")
    test_image = None

    # Look for any image in output/pieces or input
    for directory in ["../output/pieces", "../input", "."]:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    test_image = os.path.join(directory, file)
                    print(f"   Found test image: {test_image}")
                    break
            if test_image:
                break

    if not test_image:
        print("   No test image found. Please provide an image path as argument.")
        print("   Usage: python test_api.py path/to/image.jpg")
        return

    # Test 3: Try different request formats
    print(f"\n3. Testing API with image: {test_image}")

    # Format 1: Simple files parameter
    print("\n   Format 1: Simple files parameter")
    try:
        with open(test_image, 'rb') as f:
            files = {'query_image': f}
            response = requests.post(
                "https://api.brickognize.com/predict/parts/",
                files=files,
                timeout=30
            )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   SUCCESS! Response: {response.json()}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

    # Format 2: With explicit content type
    print("\n   Format 2: With explicit content type")
    try:
        with open(test_image, 'rb') as f:
            files = {'query_image': (os.path.basename(test_image), f, 'image/jpeg')}
            response = requests.post(
                "https://api.brickognize.com/predict/parts/",
                files=files,
                timeout=30
            )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   SUCCESS! Response: {response.json()}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

    # Format 3: With headers
    print("\n   Format 3: With accept header")
    try:
        with open(test_image, 'rb') as f:
            files = {'query_image': (os.path.basename(test_image), f, 'image/jpeg')}
            headers = {'accept': 'application/json'}
            response = requests.post(
                "https://api.brickognize.com/predict/parts/",
                files=files,
                headers=headers,
                timeout=30
            )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   SUCCESS! Response: {response.json()}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

    # Format 4: Try the base predict endpoint
    print("\n   Format 4: Using base /predict/ endpoint")
    try:
        with open(test_image, 'rb') as f:
            files = {'query_image': (os.path.basename(test_image), f, 'image/jpeg')}
            headers = {'accept': 'application/json'}
            response = requests.post(
                "https://api.brickognize.com/predict/",
                files=files,
                headers=headers,
                timeout=30
            )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   SUCCESS! Response: {response.json()}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Use provided image
        test_image = sys.argv[1]
        if os.path.exists(test_image):
            print(f"Using provided image: {test_image}\n")
            with open(test_image, 'rb') as f:
                files = {'query_image': (os.path.basename(test_image), f, 'image/jpeg')}
                headers = {'accept': 'application/json'}
                response = requests.post(
                    "https://api.brickognize.com/predict/",
                    files=files,
                    headers=headers,
                    timeout=30
                )
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        else:
            print(f"Error: Image not found: {test_image}")
    else:
        test_api_connection()
