"""Tests for presets module."""

import pytest
from product_image_optimizer.presets import (
    get_preset,
    get_theme,
    list_presets,
    list_themes,
)


class TestPresets:
    """Test preset configurations."""

    def test_list_presets(self):
        """Test listing presets."""
        presets = list_presets()
        assert isinstance(presets, list)
        assert len(presets) > 0
        assert "ecommerce_square" in presets

    def test_get_preset(self):
        """Test getting a preset."""
        config = get_preset("ecommerce_square")
        assert config.target_width == 2000
        assert config.target_height == 2000
        assert config.remove_background is True

    def test_get_invalid_preset(self):
        """Test getting invalid preset raises error."""
        with pytest.raises(KeyError):
            get_preset("nonexistent_preset")

    def test_all_presets_valid(self):
        """Test all presets are valid."""
        for preset_name in list_presets():
            config = get_preset(preset_name)
            assert config.target_width > 0
            assert config.target_height > 0
            assert 0 < config.fill_ratio <= 1.0


class TestThemes:
    """Test GUI themes."""

    def test_list_themes(self):
        """Test listing themes."""
        themes = list_themes()
        assert isinstance(themes, list)
        assert len(themes) > 0
        assert "default" in themes

    def test_get_theme(self):
        """Test getting a theme."""
        theme = get_theme("default")
        assert theme.name == "default"
        assert theme.primary.startswith("#")

    def test_get_invalid_theme(self):
        """Test getting invalid theme raises error."""
        with pytest.raises(KeyError):
            get_theme("nonexistent_theme")

    def test_all_themes_valid(self):
        """Test all themes are valid."""
        for theme_name in list_themes():
            theme = get_theme(theme_name)
            assert theme.primary.startswith("#")
            assert theme.dark.startswith("#")
            assert theme.text.startswith("#")
