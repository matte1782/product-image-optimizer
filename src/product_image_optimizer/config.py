"""
Configuration management for Product Image Optimizer.

Supports both programmatic configuration and YAML/JSON config files.
"""

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Dict, Any
import json


@dataclass
class ProcessingConfig:
    """Image processing configuration."""

    # Target dimensions
    target_width: int = 1000
    target_height: int = 1000

    # Processing options
    remove_background: bool = True
    auto_crop: bool = True
    crop_padding: int = 20

    # Sizing options
    fill_ratio: float = 0.80  # How much of canvas to fill
    min_dimension: int = 500  # Minimum product size

    # Output options
    output_format: str = "PNG"
    compress_level: int = 6  # PNG compression (0-9)
    optimize: bool = True

    @property
    def target_aspect(self) -> float:
        """Calculate target aspect ratio."""
        if self.target_height == 0:
            raise ValueError("target_height cannot be zero")
        return self.target_width / self.target_height

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProcessingConfig":
        """Create from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    @classmethod
    def from_json_file(cls, path: Path) -> "ProcessingConfig":
        """Load from JSON file."""
        with open(path, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_json_file(self, path: Path) -> None:
        """Save to JSON file."""
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)


@dataclass
class GUITheme:
    """GUI color theme configuration."""

    name: str = "default"
    primary: str = "#2196F3"  # Blue
    dark: str = "#1A1A1A"  # Dark background
    surface: str = "#2B2B2B"  # Surface color
    text: str = "#FFFFFF"  # Text color
    success: str = "#4CAF50"  # Success green
    warning: str = "#FF9800"  # Warning orange
    accent: str = "#64B5F6"  # Light accent

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "GUITheme":
        """Create from dictionary."""
        return cls(**data)


class ConfigManager:
    """Manages application configuration."""

    DEFAULT_CONFIG_NAME = "config.json"

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize config manager.

        Args:
            config_dir: Directory for config files. Defaults to ~/.product-image-optimizer
        """
        if config_dir is None:
            config_dir = Path.home() / ".product-image-optimizer"

        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.processing_config = ProcessingConfig()
        self.gui_theme = GUITheme()

    def load_config(self, name: str = DEFAULT_CONFIG_NAME) -> None:
        """Load configuration from file."""
        config_path = self.config_dir / name
        if config_path.exists():
            self.processing_config = ProcessingConfig.from_json_file(config_path)

    def save_config(self, name: str = DEFAULT_CONFIG_NAME) -> None:
        """Save configuration to file."""
        config_path = self.config_dir / name
        self.processing_config.to_json_file(config_path)

    def load_theme(self, name: str) -> None:
        """Load theme from file."""
        theme_path = self.config_dir / f"theme_{name}.json"
        if theme_path.exists():
            with open(theme_path, "r") as f:
                data = json.load(f)
            self.gui_theme = GUITheme.from_dict(data)

    def save_theme(self, name: str) -> None:
        """Save theme to file."""
        theme_path = self.config_dir / f"theme_{name}.json"
        with open(theme_path, "w") as f:
            json.dump(self.gui_theme.to_dict(), f, indent=2)
