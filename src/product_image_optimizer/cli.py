"""
Command-line interface for Product Image Optimizer.

Provides a powerful CLI for batch processing and automation.
"""

import argparse
import sys
from pathlib import Path
from typing import List
import zipfile

from .config import ConfigManager
from .processor import batch_process
from .presets import get_preset, list_presets, list_themes


def extract_zip(zip_path: Path) -> List[Path]:
    """Extract ZIP file and return list of image paths."""
    import tempfile

    # Use temporary directory that auto-cleans
    temp_dir = Path(tempfile.mkdtemp(prefix="product_img_opt_"))

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            # Validate ZIP entries to prevent path traversal
            for member in zip_ref.namelist():
                # Check for path traversal attempts
                if member.startswith("/") or ".." in member or member.startswith("\\"):
                    raise ValueError(f"Unsafe path in ZIP: {member}")

            # Safe to extract
            zip_ref.extractall(temp_dir)

        # Find all images
        image_files = []
        for ext in ["*.jpg", "*.jpeg", "*.png"]:
            image_files.extend(temp_dir.rglob(ext))

        return image_files
    except Exception:
        # Clean up on error
        import shutil

        shutil.rmtree(temp_dir, ignore_errors=True)
        raise


def collect_image_files(paths: List[str]) -> List[Path]:
    """Collect image files from paths (files, directories, or ZIPs)."""
    image_files = []
    supported_exts = {".jpg", ".jpeg", ".png"}

    for path_str in paths:
        path = Path(path_str)

        if not path.exists():
            print("Warning: Path not found: {}".format(path))
            continue

        if path.is_file():
            if path.suffix.lower() == ".zip":
                # Extract ZIP
                print(f"Extracting ZIP: {path}")
                extracted = extract_zip(path)
                image_files.extend(extracted)
            elif path.suffix.lower() in supported_exts:
                # Single image
                image_files.append(path)
            else:
                print("Warning: Unsupported file type: {}".format(path))

        elif path.is_dir():
            # Recursively find images in directory
            for ext in supported_exts:
                image_files.extend(path.rglob(f"*{ext}"))
                # Also check uppercase
                image_files.extend(path.rglob(f"*{ext.upper()}"))

    return image_files


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description="Product Image Optimizer - Professional image processing for e-commerce and social media",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process single image
  product-image-optimizer image.jpg -o output/

  # Batch process directory
  product-image-optimizer images/ -o output/

  # Use preset configuration
  product-image-optimizer images/ -o output/ --preset ecommerce_square

  # Custom dimensions
  product-image-optimizer images/ -o output/ -w 2000 -h 2000

  # Disable background removal
  product-image-optimizer images/ -o output/ --no-bg-removal

  # List available presets
  product-image-optimizer --list-presets

For more information, visit: https://github.com/matte1782/product-image-optimizer
        """,
    )

    # Input/Output
    parser.add_argument(
        "input", nargs="*", help="Input files, directories, or ZIP archives"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=False,
        help="Output directory (default: ./output)",
    )

    # Presets
    parser.add_argument(
        "--preset",
        type=str,
        help=f'Use preset configuration (available: {", ".join(list_presets())})',
    )
    parser.add_argument(
        "--list-presets", action="store_true", help="List all available presets"
    )
    parser.add_argument(
        "--list-themes", action="store_true", help="List all available GUI themes"
    )

    # Dimensions
    parser.add_argument(
        "-w", "--width", type=int, help="Target width in pixels (default: 1000)"
    )
    parser.add_argument(
        "--height",  # Removed -h to avoid conflict with --help
        type=int,
        help="Target height in pixels (default: 1000)",
    )

    # Processing options
    parser.add_argument(
        "--no-bg-removal", action="store_true", help="Disable background removal"
    )
    parser.add_argument(
        "--no-auto-crop", action="store_true", help="Disable auto-cropping"
    )
    parser.add_argument(
        "--fill-ratio", type=float, help="Canvas fill ratio (0.0-1.0, default: 0.80)"
    )
    parser.add_argument(
        "--padding", type=int, help="Crop padding in pixels (default: 20)"
    )

    # Output options
    parser.add_argument(
        "--format",
        type=str,
        choices=["PNG", "JPEG"],
        help="Output format (default: PNG)",
    )
    parser.add_argument(
        "--compress",
        type=int,
        choices=range(0, 10),
        metavar="0-9",
        help="PNG compression level (default: 6)",
    )
    parser.add_argument(
        "--no-optimize", action="store_true", help="Disable output optimization"
    )

    # Config management
    parser.add_argument(
        "--save-config",
        type=str,
        metavar="NAME",
        help="Save current settings as config",
    )
    parser.add_argument(
        "--load-config", type=str, metavar="NAME", help="Load settings from config"
    )

    # Misc
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--version", action="version", version="Product Image Optimizer v1.0.0"
    )

    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Handle list commands
    if args.list_presets:
        print("Available presets:")
        for preset in list_presets():
            print(f"  - {preset}")
        sys.exit(0)

    if args.list_themes:
        print("Available GUI themes:")
        for theme in list_themes():
            print(f"  - {theme}")
        sys.exit(0)

    # Require input
    if not args.input:
        parser.print_help()
        sys.exit(1)

    # Setup configuration
    config_manager = ConfigManager()

    # Load config if specified
    if args.load_config:
        try:
            config_manager.load_config(args.load_config)
            if args.verbose:
                print(f"Loaded config: {args.load_config}")
        except FileNotFoundError:
            print(f"Error: Config '{args.load_config}' not found")
            sys.exit(1)

    # Use preset if specified
    if args.preset:
        try:
            config = get_preset(args.preset)
            if args.verbose:
                print(f"Using preset: {args.preset}")
        except KeyError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        config = config_manager.processing_config

    # Apply CLI arguments (override config/preset)
    if args.width:
        config.target_width = args.width
    if args.height:
        config.target_height = args.height
    if args.no_bg_removal:
        config.remove_background = False
    if args.no_auto_crop:
        config.auto_crop = False
    if args.fill_ratio:
        if not 0.0 < args.fill_ratio <= 1.0:
            print("Error: fill-ratio must be between 0.0 and 1.0")
            sys.exit(1)
        config.fill_ratio = args.fill_ratio
    if args.padding:
        config.crop_padding = args.padding
    if args.format:
        config.output_format = args.format
    if args.compress is not None:
        config.compress_level = args.compress
    if args.no_optimize:
        config.optimize = False

    # Save config if requested
    if args.save_config:
        config_manager.processing_config = config
        config_manager.save_config(args.save_config)
        print(f"Configuration saved as: {args.save_config}")

    # Collect image files
    print("Collecting images...")
    image_files = collect_image_files(args.input)

    if not image_files:
        print("Error: No images found")
        sys.exit(1)

    print(f"Found {len(image_files)} images")

    # Setup output directory
    output_dir = Path(args.output) if args.output else Path("./output")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Print processing info
    if args.verbose:
        print("\nProcessing Configuration:")
        print(f"  Target size: {config.target_width} x {config.target_height}px")
        print(f"  Background removal: {config.remove_background}")
        print(f"  Auto-crop: {config.auto_crop}")
        print(f"  Fill ratio: {config.fill_ratio}")
        print(f"  Output format: {config.output_format}")
        print(f"  Output directory: {output_dir}\n")

    # Process images
    print("Processing images...")

    def progress_callback(current, total, filename):
        print(f"  [{current}/{total}] {filename}")

    results = batch_process(
        image_files,
        output_dir,
        config,
        progress_callback=progress_callback if args.verbose else None,
    )

    # Print results
    print("\n" + "=" * 60)
    print("Processing complete!")
    print("=" * 60)
    print(f"  Total:   {results['total']}")
    print(f"  Success: {results['success']}")
    print(f"  Failed:  {results['failed']}")
    print(f"  Output:  {output_dir.absolute()}")
    print("=" * 60)

    # Print errors if any
    if results["failed"] > 0:
        print("\nErrors:")
        for result in results["results"]:
            if not result["success"]:
                print(f"  ✗ {result['input']}: {result['error']}")

    sys.exit(0 if results["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
