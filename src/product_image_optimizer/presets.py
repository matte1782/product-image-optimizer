"""
Preset configurations for common use cases.

Includes presets for e-commerce, social media, and other common platforms.
"""

from typing import Dict
from .config import ProcessingConfig, GUITheme


# ============================================================================
# PROCESSING PRESETS
# ============================================================================

PROCESSING_PRESETS: Dict[str, ProcessingConfig] = {
    "ecommerce_square": ProcessingConfig(
        target_width=2000,
        target_height=2000,
        fill_ratio=0.85,
        remove_background=True,
        auto_crop=True,
    ),
    "ecommerce_portrait": ProcessingConfig(
        target_width=1000,
        target_height=1500,
        fill_ratio=0.80,
        remove_background=True,
        auto_crop=True,
    ),
    "instagram_square": ProcessingConfig(
        target_width=1080,
        target_height=1080,
        fill_ratio=0.90,
        remove_background=True,
        auto_crop=True,
    ),
    "instagram_portrait": ProcessingConfig(
        target_width=1080,
        target_height=1350,
        fill_ratio=0.85,
        remove_background=True,
        auto_crop=True,
    ),
    "facebook_feed": ProcessingConfig(
        target_width=1200,
        target_height=630,
        fill_ratio=0.75,
        remove_background=True,
        auto_crop=True,
    ),
    "pinterest": ProcessingConfig(
        target_width=1000,
        target_height=1500,
        fill_ratio=0.80,
        remove_background=True,
        auto_crop=True,
    ),
    "amazon_main": ProcessingConfig(
        target_width=2000,
        target_height=2000,
        fill_ratio=0.85,
        remove_background=False,  # Amazon prefers white bg
        auto_crop=True,
    ),
    "shopify_product": ProcessingConfig(
        target_width=2048,
        target_height=2048,
        fill_ratio=0.80,
        remove_background=True,
        auto_crop=True,
    ),
    "twitter_card": ProcessingConfig(
        target_width=1200,
        target_height=675,
        fill_ratio=0.70,
        remove_background=True,
        auto_crop=True,
    ),
    "thumbnail": ProcessingConfig(
        target_width=400,
        target_height=400,
        fill_ratio=0.90,
        remove_background=True,
        auto_crop=True,
        compress_level=8,  # Higher compression for thumbnails
    ),
}


# ============================================================================
# GUI THEMES
# ============================================================================

GUI_THEMES: Dict[str, GUITheme] = {
    "default": GUITheme(
        name="default",
        primary="#2196F3",
        dark="#1A1A1A",
        surface="#2B2B2B",
        text="#FFFFFF",
        success="#4CAF50",
        warning="#FF9800",
        accent="#64B5F6",
    ),
    "dark_blue": GUITheme(
        name="dark_blue",
        primary="#1976D2",
        dark="#0D1117",
        surface="#161B22",
        text="#C9D1D9",
        success="#238636",
        warning="#D29922",
        accent="#58A6FF",
    ),
    "purple": GUITheme(
        name="purple",
        primary="#9C27B0",
        dark="#1A1A1A",
        surface="#2B2B2B",
        text="#FFFFFF",
        success="#4CAF50",
        warning="#FF9800",
        accent="#BA68C8",
    ),
    "green": GUITheme(
        name="green",
        primary="#4CAF50",
        dark="#1A1A1A",
        surface="#2B2B2B",
        text="#FFFFFF",
        success="#66BB6A",
        warning="#FF9800",
        accent="#81C784",
    ),
    "orange": GUITheme(
        name="orange",
        primary="#FF5722",
        dark="#1A1A1A",
        surface="#2B2B2B",
        text="#FFFFFF",
        success="#4CAF50",
        warning="#FFA726",
        accent="#FF7043",
    ),
    "red": GUITheme(
        name="red",
        primary="#E31E24",
        dark="#1A1A1A",
        surface="#2B2B2B",
        text="#FFFFFF",
        success="#4CAF50",
        warning="#FF9800",
        accent="#FF6B6B",
    ),
    "minimal_light": GUITheme(
        name="minimal_light",
        primary="#000000",
        dark="#FFFFFF",
        surface="#F5F5F5",
        text="#000000",
        success="#2E7D32",
        warning="#F57C00",
        accent="#424242",
    ),
}


def get_preset(name: str) -> ProcessingConfig:
    """
    Get a processing preset by name.

    Args:
        name: Preset name

    Returns:
        ProcessingConfig instance

    Raises:
        KeyError: If preset not found
    """
    if name not in PROCESSING_PRESETS:
        available = ", ".join(PROCESSING_PRESETS.keys())
        raise KeyError(f"Unknown preset '{name}'. Available: {available}")

    return PROCESSING_PRESETS[name]


def get_theme(name: str) -> GUITheme:
    """
    Get a GUI theme by name.

    Args:
        name: Theme name

    Returns:
        GUITheme instance

    Raises:
        KeyError: If theme not found
    """
    if name not in GUI_THEMES:
        available = ", ".join(GUI_THEMES.keys())
        raise KeyError(f"Unknown theme '{name}'. Available: {available}")

    return GUI_THEMES[name]


def list_presets() -> list:
    """List all available presets."""
    return list(PROCESSING_PRESETS.keys())


def list_themes() -> list:
    """List all available themes."""
    return list(GUI_THEMES.keys())
