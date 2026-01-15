"""Tests for configuration module."""

import pytest
from pathlib import Path
import json
import tempfile

from product_image_optimizer.config import ProcessingConfig, GUITheme, ConfigManager


class TestProcessingConfig:
    """Test ProcessingConfig."""

    def test_default_config(self):
        """Test default configuration."""
        config = ProcessingConfig()
        assert config.target_width == 1000
        assert config.target_height == 1000
        assert config.remove_background is True
        assert config.auto_crop is True

    def test_target_aspect(self):
        """Test aspect ratio calculation."""
        config = ProcessingConfig(target_width=1000, target_height=2000)
        assert config.target_aspect == 0.5

    def test_custom_config(self):
        """Test custom configuration."""
        config = ProcessingConfig(
            target_width=2000,
            target_height=3000,
            fill_ratio=0.9,
            remove_background=False,
        )
        assert config.target_width == 2000
        assert config.target_height == 3000
        assert config.fill_ratio == 0.9
        assert config.remove_background is False

    def test_to_dict(self):
        """Test converting to dictionary."""
        config = ProcessingConfig(target_width=1500)
        data = config.to_dict()
        assert isinstance(data, dict)
        assert data["target_width"] == 1500

    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {"target_width": 1500, "target_height": 2000}
        config = ProcessingConfig.from_dict(data)
        assert config.target_width == 1500
        assert config.target_height == 2000

    def test_json_roundtrip(self):
        """Test JSON save/load roundtrip."""
        config = ProcessingConfig(target_width=2500, fill_ratio=0.75)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = Path(f.name)

        try:
            config.to_json_file(temp_path)
            loaded_config = ProcessingConfig.from_json_file(temp_path)

            assert loaded_config.target_width == 2500
            assert loaded_config.fill_ratio == 0.75
        finally:
            temp_path.unlink()


class TestGUITheme:
    """Test GUITheme."""

    def test_default_theme(self):
        """Test default theme."""
        theme = GUITheme()
        assert theme.name == "default"
        assert theme.primary == "#2196F3"
        assert theme.text == "#FFFFFF"

    def test_custom_theme(self):
        """Test custom theme."""
        theme = GUITheme(name="test", primary="#FF0000")
        assert theme.name == "test"
        assert theme.primary == "#FF0000"

    def test_theme_dict(self):
        """Test theme dictionary conversion."""
        theme = GUITheme(name="test", primary="#FF0000")
        data = theme.to_dict()
        assert data["name"] == "test"
        assert data["primary"] == "#FF0000"


class TestConfigManager:
    """Test ConfigManager."""

    def test_default_manager(self):
        """Test default config manager."""
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ConfigManager(config_dir=Path(temp_dir))
            assert manager.config_dir.exists()
            assert isinstance(manager.processing_config, ProcessingConfig)
            assert isinstance(manager.gui_theme, GUITheme)

    def test_save_load_config(self):
        """Test saving and loading config."""
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = ConfigManager(config_dir=Path(temp_dir))
            manager.processing_config.target_width = 3000

            manager.save_config("test.json")
            manager.processing_config.target_width = 1000  # Change it
            manager.load_config("test.json")

            assert manager.processing_config.target_width == 3000
