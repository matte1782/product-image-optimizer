"""
Product Image Optimizer
========================

Professional image processing for e-commerce and social media.

Features:
- AI-powered background removal
- Intelligent resizing and centering
- Preset configurations for major platforms
- Both CLI and GUI interfaces
- Batch processing support

Quick Start:
    # Python API
    >>> from product_image_optimizer import ImageProcessor, ProcessingConfig
    >>> config = ProcessingConfig(target_width=2000, target_height=2000)
    >>> processor = ImageProcessor(config)
    >>> processor.process_image("input.jpg", "output.png")

    # CLI
    $ product-image-optimizer images/ -o output/ --preset ecommerce_square

    # GUI
    $ product-image-optimizer-gui

Author: Your Name
License: MIT
Repository: https://github.com/matte1782/product-image-optimizer
"""

__version__ = "1.0.0"
__author__ = "Matteo Panzeri"
__license__ = "MIT"

from .config import ProcessingConfig, GUITheme, ConfigManager
from .processor import ImageProcessor, batch_process
from .presets import (
    PROCESSING_PRESETS,
    GUI_THEMES,
    get_preset,
    get_theme,
    list_presets,
    list_themes,
)
from .cli import main as cli_main
from .gui import launch_gui

__all__ = [
    # Core
    "ImageProcessor",
    "ProcessingConfig",
    "GUITheme",
    "ConfigManager",
    "batch_process",
    # Presets
    "PROCESSING_PRESETS",
    "GUI_THEMES",
    "get_preset",
    "get_theme",
    "list_presets",
    "list_themes",
    # Interfaces
    "cli_main",
    "launch_gui",
    # Metadata
    "__version__",
    "__author__",
    "__license__",
]
