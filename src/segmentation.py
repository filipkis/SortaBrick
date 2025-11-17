"""
Image segmentation module for detecting and extracting individual LEGO pieces.
"""
import cv2
import numpy as np
from typing import List, Tuple
import os


class LegoSegmenter:
    """Segments images containing multiple LEGO pieces into individual pieces."""

    def __init__(self, min_area: int = 500, max_area: int = 100000, padding: int = 10):
        """
        Initialize the LEGO segmenter.

        Args:
            min_area: Minimum contour area to consider as a LEGO piece (filters noise)
            max_area: Maximum contour area to consider as a LEGO piece
            padding: Pixels to add around each detected piece when cropping
        """
        self.min_area = min_area
        self.max_area = max_area
        self.padding = padding

    def detect_pieces(self, image_path: str) -> Tuple[np.ndarray, List[Tuple[int, int, int, int]]]:
        """
        Detect individual LEGO pieces in an image.

        Args:
            image_path: Path to the input image

        Returns:
            Tuple of (original_image, list of bounding boxes as (x, y, w, h))
        """
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply adaptive thresholding for better segmentation
        # This works better than simple thresholding for varying lighting
        thresh = cv2.adaptiveThreshold(
            blurred, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11, 2
        )

        # Apply morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter contours by area and get bounding boxes
        bounding_boxes = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.min_area < area < self.max_area:
                x, y, w, h = cv2.boundingRect(contour)
                bounding_boxes.append((x, y, w, h))

        # Sort bounding boxes from left to right, top to bottom
        bounding_boxes.sort(key=lambda box: (box[1] // 100, box[0]))

        return image, bounding_boxes

    def extract_pieces(self, image: np.ndarray, bounding_boxes: List[Tuple[int, int, int, int]],
                       output_dir: str, base_name: str = "piece") -> List[str]:
        """
        Extract individual pieces from the image and save them.

        Args:
            image: The original image
            bounding_boxes: List of bounding boxes (x, y, w, h)
            output_dir: Directory to save extracted pieces
            base_name: Base name for output files

        Returns:
            List of paths to saved piece images
        """
        os.makedirs(output_dir, exist_ok=True)
        saved_paths = []

        height, width = image.shape[:2]

        for idx, (x, y, w, h) in enumerate(bounding_boxes):
            # Add padding around the piece
            x1 = max(0, x - self.padding)
            y1 = max(0, y - self.padding)
            x2 = min(width, x + w + self.padding)
            y2 = min(height, y + h + self.padding)

            # Extract the piece
            piece = image[y1:y2, x1:x2]

            # Save the piece
            output_path = os.path.join(output_dir, f"{base_name}_{idx:03d}.jpg")
            cv2.imwrite(output_path, piece)
            saved_paths.append(output_path)

        return saved_paths

    def visualize_detection(self, image: np.ndarray, bounding_boxes: List[Tuple[int, int, int, int]],
                           output_path: str = None) -> np.ndarray:
        """
        Draw bounding boxes on the image for visualization.

        Args:
            image: The original image
            bounding_boxes: List of bounding boxes (x, y, w, h)
            output_path: Optional path to save the visualization

        Returns:
            Image with drawn bounding boxes
        """
        vis_image = image.copy()

        for idx, (x, y, w, h) in enumerate(bounding_boxes):
            # Draw rectangle
            cv2.rectangle(vis_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Add label
            cv2.putText(vis_image, f"{idx}", (x, y - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if output_path:
            cv2.imwrite(output_path, vis_image)

        return vis_image
