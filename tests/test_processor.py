"""Tests for processor module."""

import pytest
from pathlib import Path
import tempfile
from PIL import Image

from product_image_optimizer.processor import ImageProcessor
from product_image_optimizer.config import ProcessingConfig


@pytest.fixture
def test_image():
    """Create a test image."""
    img = Image.new("RGB", (1000, 1000), color="red")
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
        temp_path = Path(f.name)
    img.save(temp_path)
    yield temp_path
    temp_path.unlink()


@pytest.fixture
def test_image_with_alpha():
    """Create a test image with alpha channel."""
    img = Image.new("RGBA", (1000, 1000), color=(255, 0, 0, 255))
    # Add transparent padding
    for x in range(0, 200):
        for y in range(1000):
            img.putpixel((x, y), (0, 0, 0, 0))
    for x in range(800, 1000):
        for y in range(1000):
            img.putpixel((x, y), (0, 0, 0, 0))

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        temp_path = Path(f.name)
    img.save(temp_path)
    yield temp_path
    temp_path.unlink()


class TestImageProcessor:
    """Test ImageProcessor."""

    def test_default_processor(self):
        """Test creating processor with default config."""
        processor = ImageProcessor()
        assert processor.config.target_width == 1000
        assert processor.config.target_height == 1000

    def test_custom_processor(self):
        """Test creating processor with custom config."""
        config = ProcessingConfig(target_width=2000, target_height=2000)
        processor = ImageProcessor(config)
        assert processor.config.target_width == 2000

    def test_auto_crop_transparent(self, test_image_with_alpha):
        """Test auto-cropping transparent areas."""
        processor = ImageProcessor()
        img = Image.open(test_image_with_alpha)
        cropped = processor.auto_crop_transparent(img, padding=0)

        # Should have cropped some transparent areas
        assert cropped.width < img.width

    def test_resize_to_target(self):
        """Test resizing to target dimensions."""
        config = ProcessingConfig(target_width=500, target_height=500)
        processor = ImageProcessor(config)

        img = Image.new("RGBA", (1000, 1000), color=(255, 0, 0, 255))
        resized = processor.resize_to_target(img)

        # Output should match target dimensions
        assert resized.size == (500, 500)
        assert resized.mode == "RGBA"

    def test_process_image_no_bg_removal(self, test_image):
        """Test processing without background removal."""
        config = ProcessingConfig(
            target_width=800, target_height=800, remove_background=False
        )
        processor = ImageProcessor(config)

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "output.png"
            success, error, metadata = processor.process_image(test_image, output_path)

            assert success is True
            assert error is None
            assert output_path.exists()
            assert metadata["output_size"] == (800, 800)

            # Check output image
            output_img = Image.open(output_path)
            assert output_img.size == (800, 800)

    def test_process_image_metadata(self, test_image):
        """Test that metadata is returned correctly."""
        config = ProcessingConfig(remove_background=False)
        processor = ImageProcessor(config)

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "output.png"
            success, error, metadata = processor.process_image(test_image, output_path)

            assert "original_size" in metadata
            assert "output_size" in metadata
            assert "file_size_kb" in metadata
            assert metadata["file_size_kb"] > 0

    def test_process_invalid_image(self):
        """Test processing invalid image file."""
        processor = ImageProcessor()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a non-image file
            input_path = Path(temp_dir) / "not_an_image.jpg"
            input_path.write_text("This is not an image")

            output_path = Path(temp_dir) / "output.png"
            success, error, metadata = processor.process_image(input_path, output_path)

            assert success is False
            assert error is not None
