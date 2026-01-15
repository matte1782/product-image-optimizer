"""
Core image processing module.

Handles background removal, resizing, cropping, and optimization.
"""

from pathlib import Path
from typing import Optional, Callable, Tuple, List
from PIL import Image
from rembg import remove

from .config import ProcessingConfig


class ImageProcessor:
    """
    Core image processor with configurable pipeline.

    Handles:
    - Background removal (optional)
    - Auto-cropping to product bounds
    - Intelligent resizing
    - Professional centering
    - Output optimization
    """

    def __init__(self, config: Optional[ProcessingConfig] = None):
        """
        Initialize processor.

        Args:
            config: Processing configuration. Uses defaults if not provided.
        """
        self.config = config or ProcessingConfig()

    def auto_crop_transparent(
        self, img: Image.Image, padding: Optional[int] = None
    ) -> Image.Image:
        """
        Auto-crop image to transparent bounds with optional padding.

        Args:
            img: PIL Image with RGBA mode
            padding: Pixels to add around crop bounds. Uses config default if None.

        Returns:
            Cropped image
        """
        if img.mode != "RGBA":
            return img

        padding = padding if padding is not None else self.config.crop_padding

        bbox = img.getbbox()
        if bbox:
            left = max(0, bbox[0] - padding)
            top = max(0, bbox[1] - padding)
            right = min(img.width, bbox[2] + padding)
            bottom = min(img.height, bbox[3] + padding)
            return img.crop((left, top, right, bottom))

        return img

    def resize_to_target(self, img: Image.Image) -> Image.Image:
        """
        Intelligent product-focused resizing algorithm.

        Algorithm:
        1. Auto-crop to product bounds
        2. Calculate optimal size to fill canvas (respecting fill_ratio)
        3. Ensure minimum dimensions
        4. Resize with high-quality resampling
        5. Center on canvas

        Args:
            img: PIL Image (RGBA mode recommended)

        Returns:
            Resized and centered image on target canvas
        """
        # Step 1: Auto-crop if enabled
        if self.config.auto_crop:
            img_cropped = self.auto_crop_transparent(img)
        else:
            img_cropped = img

        current_width, current_height = img_cropped.size

        # Validate dimensions after cropping
        if current_width <= 0 or current_height <= 0:
            raise ValueError(
                f"Image has invalid dimensions after cropping: {current_width}x{current_height}"
            )

        current_aspect = current_width / current_height

        # Step 2: Calculate resize to use fill_ratio of canvas
        available_width = int(self.config.target_width * self.config.fill_ratio)
        available_height = int(self.config.target_height * self.config.fill_ratio)

        # Validate calculated dimensions
        if available_width <= 0 or available_height <= 0:
            raise ValueError(
                f"Invalid dimensions after applying fill_ratio: {available_width}x{available_height}"
            )

        if current_aspect > (available_width / available_height):
            # Width-constrained
            new_width = available_width
            new_height = int(available_width / current_aspect)
        else:
            # Height-constrained
            new_height = available_height
            new_width = int(available_height * current_aspect)

        # Step 3: Ensure minimum dimensions
        if min(new_width, new_height) < self.config.min_dimension:
            scale_factor = self.config.min_dimension / min(new_width, new_height)
            new_width = int(new_width * scale_factor)
            new_height = int(new_height * scale_factor)

            # Respect canvas boundaries (max 95% to keep margins)
            max_width = int(self.config.target_width * 0.95)
            max_height = int(self.config.target_height * 0.95)

            if new_width > max_width:
                scale = max_width / new_width
                new_width = max_width
                new_height = int(new_height * scale)

            if new_height > max_height:
                scale = max_height / new_height
                new_height = max_height
                new_width = int(new_width * scale)

        # Step 4: Resize with high quality
        img_resized = img_cropped.resize(
            (new_width, new_height), Image.Resampling.LANCZOS
        )

        # Step 5: Create canvas and center
        canvas = Image.new(
            "RGBA", (self.config.target_width, self.config.target_height), (0, 0, 0, 0)
        )

        paste_x = (self.config.target_width - new_width) // 2
        paste_y = (self.config.target_height - new_height) // 2
        canvas.paste(img_resized, (paste_x, paste_y), img_resized)

        return canvas

    def remove_background(self, img: Image.Image) -> Image.Image:
        """
        Remove image background using AI (rembg/U²-Net).

        Args:
            img: PIL Image

        Returns:
            Image with transparent background (RGBA mode)
        """
        try:
            # Ensure RGB mode for rembg
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Remove background
            output = remove(img)
            return output

        except (OSError, IOError, RuntimeError, ValueError) as e:
            # Handle expected errors from rembg or PIL
            print(f"Background removal failed: {e}")
            # Fallback: convert to RGBA without removal
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            return img

    def process_image(
        self,
        input_path: Path,
        output_path: Path,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> Tuple[bool, Optional[str], Optional[dict]]:
        """
        Process a single image through the full pipeline.

        Pipeline:
        1. Load image
        2. Remove background (if enabled)
        3. Resize and center
        4. Save optimized output

        Args:
            input_path: Path to input image
            output_path: Path for output image
            progress_callback: Optional callback for progress updates

        Returns:
            Tuple of (success, error_message, metadata)
            - success: True if processing succeeded
            - error_message: Error string if failed, None otherwise
            - metadata: Dict with file_size_kb, dimensions, etc.
        """
        metadata = {
            "input": str(input_path),
            "output": str(output_path),
            "config": self.config.to_dict(),
        }

        try:
            # Load image with context manager to ensure proper cleanup
            if progress_callback:
                progress_callback(f"Loading: {input_path.name}")

            with Image.open(input_path) as img:
                metadata["original_size"] = img.size
                metadata["original_mode"] = img.mode

                # Load the image data (PIL uses lazy loading)
                img.load()

                # Step 1: Remove background
                if self.config.remove_background:
                    if progress_callback:
                        progress_callback(f"Removing background: {input_path.name}")

                    img_no_bg = self.remove_background(img)
                else:
                    # Ensure RGBA mode
                    img_no_bg = (
                        img.convert("RGBA") if img.mode != "RGBA" else img.copy()
                    )

            # Step 2: Resize to target
            if progress_callback:
                progress_callback(f"Resizing: {input_path.name}")

            img_resized = self.resize_to_target(img_no_bg)
            metadata["output_size"] = img_resized.size

            # Step 3: Save optimized output
            if progress_callback:
                progress_callback(f"Saving: {output_path.name}")

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            img_resized.save(
                output_path,
                format=self.config.output_format,
                optimize=self.config.optimize,
                compress_level=self.config.compress_level,
            )

            # Get output file stats
            metadata["file_size_kb"] = output_path.stat().st_size / 1024

            return True, None, metadata

        except (OSError, IOError, ValueError, RuntimeError) as e:
            error_msg = f"Processing failed for {input_path.name}: {str(e)}"
            return False, error_msg, metadata
        except Exception as e:
            # Unexpected errors - re-raise for debugging
            error_msg = f"Unexpected error processing {input_path.name}: {str(e)}"
            return False, error_msg, metadata


def batch_process(
    input_paths: List[Path],
    output_dir: Path,
    config: Optional[ProcessingConfig] = None,
    progress_callback: Optional[Callable[[int, int, str], None]] = None,
) -> dict:
    """
    Batch process multiple images.

    Args:
        input_paths: List of input image paths
        output_dir: Output directory
        config: Processing configuration
        progress_callback: Callback(current, total, filename)

    Returns:
        Dict with success/failed counts and results list
    """
    processor = ImageProcessor(config)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = {"total": len(input_paths), "success": 0, "failed": 0, "results": []}

    for i, input_path in enumerate(input_paths, 1):
        # Generate output filename
        output_path = output_dir / f"{input_path.stem}.png"

        # Progress callback
        if progress_callback:
            progress_callback(i, len(input_paths), input_path.name)

        # Process
        success, error, metadata = processor.process_image(input_path, output_path)

        if success:
            results["success"] += 1
        else:
            results["failed"] += 1

        results["results"].append(
            {
                "input": str(input_path),
                "output": str(output_path),
                "success": success,
                "error": error,
                "metadata": metadata,
            }
        )

    return results
