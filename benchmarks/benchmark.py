"""
Performance benchmarks for Product Image Optimizer.

Tests processing speed at various image sizes.
"""

import time
from pathlib import Path
import tempfile
from PIL import Image
import json

from product_image_optimizer.processor import ImageProcessor
from product_image_optimizer.config import ProcessingConfig


def create_test_image(width, height):
    """Create a test image with random content."""
    import random
    img = Image.new('RGB', (width, height))
    pixels = img.load()
    for i in range(width):
        for j in range(height):
            pixels[i, j] = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
    return img


def benchmark_processing(image_size, config, iterations=3):
    """Benchmark image processing."""
    width, height = image_size
    times = []

    for _ in range(iterations):
        # Create test image
        img = create_test_image(width, height)

        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.jpg"
            output_path = Path(temp_dir) / "output.png"

            img.save(input_path, quality=95)

            processor = ImageProcessor(config)

            start = time.time()
            success, error, metadata = processor.process_image(input_path, output_path)
            elapsed = time.time() - start

            if success:
                times.append(elapsed)

    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        return {
            'avg': round(avg_time, 3),
            'min': round(min_time, 3),
            'max': round(max_time, 3)
        }
    return None


def run_benchmarks():
    """Run full benchmark suite."""
    print("=" * 60)
    print("Product Image Optimizer - Performance Benchmarks")
    print("=" * 60)
    print()

    test_sizes = [
        (500, 500, "Small (500x500)"),
        (1000, 1000, "Medium (1000x1000)"),
        (2000, 2000, "Large (2000x2000)"),
        (3000, 3000, "X-Large (3000x3000)"),
        (5000, 5000, "XX-Large (5000x5000)"),
    ]

    config = ProcessingConfig(
        target_width=1000,
        target_height=1000,
        remove_background=True,
        auto_crop=True
    )

    results = []

    for width, height, label in test_sizes:
        print(f"Testing {label}...", end=" ", flush=True)
        benchmark = benchmark_processing((width, height), config, iterations=3)

        if benchmark:
            print(f"avg: {benchmark['avg']}s (min: {benchmark['min']}s, max: {benchmark['max']}s)")
            results.append({
                'size': label,
                'dimensions': f"{width}x{height}",
                'avg_time_s': benchmark['avg'],
                'min_time_s': benchmark['min'],
                'max_time_s': benchmark['max']
            })
        else:
            print("FAILED")

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print()
    print(f"{'Size':<20} {'Dimensions':<15} {'Avg Time':<12}")
    print("-" * 60)
    for result in results:
        print(f"{result['size']:<20} {result['dimensions']:<15} {result['avg_time_s']:.3f}s")

    # Save results
    output_file = Path(__file__).parent / "results" / "benchmark_results.json"
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print()
    print(f"Results saved to: {output_file}")


if __name__ == '__main__':
    run_benchmarks()
