"""
Rebrickable API client for fetching LEGO part information and images.
"""
import requests
import os
import time
from typing import Dict, Optional


class RebrickableClient:
    """Client for interacting with the Rebrickable API."""

    def __init__(self, api_key: str = None):
        """
        Initialize the Rebrickable API client.

        Args:
            api_key: Rebrickable API key. If not provided, will try to read from
                    REBRICKABLE_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get('REBRICKABLE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Rebrickable API key required. Set REBRICKABLE_API_KEY environment variable "
                "or pass api_key parameter. Get your free API key at: "
                "https://rebrickable.com/api/"
            )

        self.base_url = "https://rebrickable.com/api/v3/lego"
        self.headers = {
            'Authorization': f'key {self.api_key}',
            'Accept': 'application/json'
        }
        self.cache = {}  # Simple in-memory cache
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests to be respectful

    def _rate_limit(self):
        """Simple rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()

    def get_part_info(self, part_num: str) -> Optional[Dict]:
        """
        Get part information including image URL from Rebrickable.

        Args:
            part_num: The part number (e.g., "3001")

        Returns:
            Dictionary with part info including 'part_img_url' or None if not found
        """
        # Check cache first
        if part_num in self.cache:
            return self.cache[part_num]

        # Rate limit
        self._rate_limit()

        url = f"{self.base_url}/parts/{part_num}/"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                # Extract relevant info
                part_info = {
                    'part_num': data.get('part_num'),
                    'name': data.get('name'),
                    'part_img_url': data.get('part_img_url'),
                    'part_url': data.get('part_url'),
                    'category_id': data.get('part_cat_id'),
                    'material': data.get('part_material')
                }
                # Cache the result
                self.cache[part_num] = part_info
                return part_info
            elif response.status_code == 404:
                # Part not found
                self.cache[part_num] = None
                return None
            else:
                print(f"Warning: Rebrickable API returned status {response.status_code} for part {part_num}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Warning: Failed to fetch Rebrickable data for {part_num}: {e}")
            return None

    def get_parts_batch(self, part_nums: list) -> Dict[str, Optional[Dict]]:
        """
        Get information for multiple parts.

        Args:
            part_nums: List of part numbers

        Returns:
            Dictionary mapping part_num to part_info
        """
        results = {}
        total = len(part_nums)

        for idx, part_num in enumerate(part_nums, 1):
            if idx % 10 == 0:  # Progress update every 10 parts
                print(f"  Fetching part info: {idx}/{total}")

            results[part_num] = self.get_part_info(part_num)

        return results


def get_api_key_from_file(filepath: str = ".rebrickable_key") -> Optional[str]:
    """
    Try to read API key from a file.

    Args:
        filepath: Path to file containing API key

    Returns:
        API key or None if file doesn't exist
    """
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Warning: Could not read API key from {filepath}: {e}")
    return None
