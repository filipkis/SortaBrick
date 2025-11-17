"""
Brickognize API client for LEGO piece identification.
"""
import requests
from typing import Dict, List, Optional
import time
import os


class BrickognizeClient:
    """Client for interacting with the Brickognize API."""

    def __init__(self, api_url: str = "https://api.brickognize.com", delay_between_requests: float = 1.0):
        """
        Initialize the Brickognize API client.

        Args:
            api_url: Base URL for the Brickognize API
            delay_between_requests: Delay in seconds between API requests (to be respectful)
        """
        self.api_url = api_url
        self.delay_between_requests = delay_between_requests
        self.last_request_time = 0

    def _wait_for_rate_limit(self):
        """Implement a simple rate limiting mechanism."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.delay_between_requests:
            time.sleep(self.delay_between_requests - time_since_last_request)
        self.last_request_time = time.time()

    def identify_piece(self, image_path: str, category: str = "parts") -> Dict:
        """
        Identify a LEGO piece from an image.

        Args:
            image_path: Path to the image file
            category: Category to search in ('parts', 'sets', or 'figs')
                     Use 'parts' for individual LEGO pieces (default)

        Returns:
            Dictionary containing identification results
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Map category to the appropriate endpoint
        endpoint_map = {
            "parts": "/predict/parts/",
            "sets": "/predict/sets/",
            "figs": "/predict/figs/",
            "general": "/predict/"
        }

        endpoint = endpoint_map.get(category, "/predict/parts/")

        # Wait for rate limiting
        self._wait_for_rate_limit()

        # Prepare the request
        url = f"{self.api_url}{endpoint}"

        try:
            # Determine content type based on file extension
            ext = os.path.splitext(image_path)[1].lower()
            content_type_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.bmp': 'image/bmp'
            }
            content_type = content_type_map.get(ext, 'image/jpeg')

            with open(image_path, 'rb') as image_file:
                # Use tuple format: (filename, file_object, content_type)
                files = {
                    'query_image': (os.path.basename(image_path), image_file, content_type)
                }
                headers = {'accept': 'application/json'}
                response = requests.post(url, files=files, headers=headers, timeout=30)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            # More detailed error for HTTP errors
            error_msg = f"HTTP {response.status_code}: {response.text}"
            return {
                "error": error_msg,
                "status_code": response.status_code,
                "image_path": image_path,
                "success": False
            }
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "image_path": image_path,
                "success": False
            }

    def identify_multiple_pieces(self, image_paths: List[str], category: str = "parts",
                                 progress_callback=None) -> List[Dict]:
        """
        Identify multiple LEGO pieces from a list of image paths.

        Args:
            image_paths: List of paths to image files
            category: Category to search in ('parts', 'sets', or 'figs')
            progress_callback: Optional callback function(current, total, result) for progress updates

        Returns:
            List of dictionaries containing identification results for each image
        """
        results = []
        total = len(image_paths)

        for idx, image_path in enumerate(image_paths):
            print(f"Identifying piece {idx + 1}/{total}: {os.path.basename(image_path)}")

            result = self.identify_piece(image_path, category)
            result['image_path'] = image_path
            result['piece_index'] = idx

            results.append(result)

            if progress_callback:
                progress_callback(idx + 1, total, result)

        return results

    def format_result(self, result: Dict, top_n: int = 5) -> str:
        """
        Format an identification result for display.

        Args:
            result: Result dictionary from identify_piece
            top_n: Number of top predictions to include

        Returns:
            Formatted string representation of the result
        """
        if "error" in result:
            return f"Error: {result['error']}"

        output = [f"\nResults for: {os.path.basename(result.get('image_path', 'Unknown'))}"]
        output.append("=" * 60)

        # Check if we have items in the result
        items = result.get('items', [])
        if not items:
            output.append("No items found")
            return "\n".join(output)

        # Display top N results
        for idx, item in enumerate(items[:top_n]):
            output.append(f"\n#{idx + 1}:")
            output.append(f"  ID: {item.get('id', 'N/A')}")
            output.append(f"  Type: {item.get('type', 'N/A')}")
            output.append(f"  Confidence: {item.get('score', 0) * 100:.2f}%")

            # Add additional info if available
            if 'name' in item:
                output.append(f"  Name: {item['name']}")

        return "\n".join(output)


def format_results_summary(results: List[Dict], output_file: str = None) -> str:
    """
    Create a summary of all identification results.

    Args:
        results: List of result dictionaries
        output_file: Optional file path to save the summary

    Returns:
        Formatted summary string
    """
    summary = ["=" * 80]
    summary.append("LEGO PIECE IDENTIFICATION SUMMARY")
    summary.append("=" * 80)
    summary.append(f"\nTotal pieces processed: {len(results)}")

    successful = sum(1 for r in results if "error" not in r and r.get('items'))
    failed = len(results) - successful

    summary.append(f"Successfully identified: {successful}")
    summary.append(f"Failed to identify: {failed}")
    summary.append("\n" + "=" * 80)

    # Individual results
    for result in results:
        client = BrickognizeClient()
        summary.append(client.format_result(result))

    summary_text = "\n".join(summary)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(summary_text)

    return summary_text
