"""
Create demo images for the README.

This script creates simple example images to demonstrate the tool's capabilities.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def create_product_image(output_path: Path, size=(2000, 2000), color=(200, 50, 50)):
    """Create a simple product-like image."""
    # Create image with white background
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)

    # Calculate product dimensions (centered, 60% of canvas)
    margin = int(size[0] * 0.2)
    product_size = size[0] - 2 * margin

    # Draw a simple product shape (rounded rectangle)
    product_rect = [
        margin,
        margin,
        margin + product_size,
        margin + product_size
    ]

    # Draw product with gradient effect (simple shading)
    for i in range(product_size):
        shade = int(i / product_size * 50)
        current_color = tuple(max(0, c - shade) for c in color)
        draw.rectangle(
            [margin + i, margin, margin + i + 1, margin + product_size],
            fill=current_color
        )

    # Add some details (simple shapes to simulate product details)
    detail_color = tuple(max(0, c - 30) for c in color)

    # Top highlight
    highlight_y = margin + int(product_size * 0.2)
    draw.rectangle(
        [margin + int(product_size * 0.2), highlight_y,
         margin + int(product_size * 0.8), highlight_y + 50],
        fill=(255, 255, 255, 128)
    )

    # Save
    img.save(output_path, quality=95)
    print(f"Created: {output_path}")


def create_comparison_image():
    """Create before/after comparison."""
    # Create input directory
    input_dir = Path(__file__).parent / "input"
    input_dir.mkdir(exist_ok=True)

    # Create sample images
    colors = [
        (220, 60, 60),   # Red product
        (60, 120, 220),  # Blue product
        (220, 180, 60),  # Yellow product
    ]

    for i, color in enumerate(colors, 1):
        output_path = input_dir / f"product_{i}.jpg"
        create_product_image(output_path, size=(2500, 2500), color=color)

    print("\n✅ Demo images created in examples/input/")
    print("Run the optimizer to generate output images:")
    print("  product-image-optimizer examples/input/ -o examples/output/ --preset ecommerce_square")


if __name__ == '__main__':
    create_comparison_image()
