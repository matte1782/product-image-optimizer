# 🖼️ Product Image Optimizer

**Professional image processing for e-commerce and social media**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Transform product images into perfectly sized, background-removed, professional photos ready for your online store or social media in seconds.

## ✨ Features

### Core Capabilities
- 🤖 **AI-Powered Background Removal** - Automatic background removal using U²-Net
- 📐 **Intelligent Resizing** - Smart cropping and centering with configurable aspect ratios
- ⚡ **Batch Processing** - Process hundreds of images in one go
- 🎨 **Professional Quality** - High-quality resampling and PNG optimization
- 🔧 **Highly Configurable** - Preset configs for major platforms or fully custom settings

### Interfaces
- 💻 **Command Line Interface** - Perfect for automation and batch jobs
- 🖱️ **Modern GUI** - Beautiful drag & drop interface with real-time progress
- 🐍 **Python API** - Integrate into your own workflows

### Platform Presets
Pre-configured for:
- **E-commerce**: Shopify, Amazon, WooCommerce
- **Social Media**: Instagram, Facebook, Pinterest, Twitter
- **Custom**: Fully configurable dimensions and settings

---

## 🚀 Quick Start

### Installation

```bash
# Install from source
git clone https://github.com/matte1782/product-image-optimizer.git
cd product-image-optimizer
pip install -e .

# With GUI support
pip install -e ".[gui]"

# With dev tools
pip install -e ".[dev]"
```

### Basic Usage

**CLI - Single image:**
```bash
product-image-optimizer image.jpg -o output/
```

**CLI - Batch process directory:**
```bash
product-image-optimizer images/ -o output/ --preset ecommerce_square
```

**GUI:**
```bash
product-image-optimizer-gui
```

**Python API:**
```python
from product_image_optimizer import ImageProcessor, get_preset

# Use preset
config = get_preset("ecommerce_square")
processor = ImageProcessor(config)
processor.process_image("input.jpg", "output.png")

# Custom configuration
from product_image_optimizer import ProcessingConfig

config = ProcessingConfig(
    target_width=2000,
    target_height=2000,
    remove_background=True,
    fill_ratio=0.85
)
processor = ImageProcessor(config)
processor.process_image("input.jpg", "output.png")
```

---

## 📖 Documentation

### CLI Reference

```bash
product-image-optimizer [input] -o [output] [options]

Positional:
  input                 Input files, directories, or ZIP archives

Options:
  -o, --output DIR      Output directory (default: ./output)
  --preset NAME         Use preset configuration
  -w, --width PX        Target width in pixels
  -h, --height PX       Target height in pixels
  --no-bg-removal       Disable background removal
  --no-auto-crop        Disable auto-cropping
  --fill-ratio 0.0-1.0  Canvas fill ratio (default: 0.80)
  --format PNG|JPEG     Output format (default: PNG)
  --compress 0-9        PNG compression level (default: 6)
  -v, --verbose         Verbose output

Presets:
  --list-presets        Show all available presets
  --list-themes         Show all GUI themes
```

### Available Presets

| Preset | Dimensions | Use Case |
|--------|-----------|----------|
| `ecommerce_square` | 2000x2000 | General e-commerce (Shopify, Etsy) |
| `ecommerce_portrait` | 1000x1500 | Portrait product shots |
| `instagram_square` | 1080x1080 | Instagram feed posts |
| `instagram_portrait` | 1080x1350 | Instagram vertical posts |
| `facebook_feed` | 1200x630 | Facebook link previews |
| `pinterest` | 1000x1500 | Pinterest pins |
| `amazon_main` | 2000x2000 | Amazon main product images |
| `shopify_product` | 2048x2048 | Shopify product photos |
| `twitter_card` | 1200x675 | Twitter card images |
| `thumbnail` | 400x400 | Small thumbnails |

### Python API

```python
from product_image_optimizer import (
    ImageProcessor,
    ProcessingConfig,
    batch_process,
    get_preset,
    list_presets
)

# List available presets
presets = list_presets()
print(presets)

# Get preset configuration
config = get_preset("instagram_square")

# Create custom configuration
config = ProcessingConfig(
    target_width=2000,
    target_height=2000,
    remove_background=True,
    auto_crop=True,
    crop_padding=20,
    fill_ratio=0.80,
    min_dimension=500,
    output_format="PNG",
    compress_level=6,
    optimize=True
)

# Process single image
processor = ImageProcessor(config)
success, error, metadata = processor.process_image(
    Path("input.jpg"),
    Path("output.png")
)

# Batch process
from pathlib import Path

results = batch_process(
    input_paths=[Path("img1.jpg"), Path("img2.jpg")],
    output_dir=Path("output/"),
    config=config,
    progress_callback=lambda current, total, name: print(f"{current}/{total}: {name}")
)

print(f"Processed: {results['success']}/{results['total']}")
```

---

## 🎯 Use Cases

### E-commerce Store Owner
**Problem:** You have 500 product photos with inconsistent backgrounds and sizes.

**Solution:**
```bash
product-image-optimizer products/ -o shopify-ready/ --preset shopify_product
```
Result: All images perfectly sized (2048x2048px), transparent background, ready for upload.

---

### Social Media Manager
**Problem:** Need to resize brand photos for Instagram, Facebook, and Twitter.

**Solution:**
```bash
product-image-optimizer photo.jpg -o instagram/ --preset instagram_square
product-image-optimizer photo.jpg -o facebook/ --preset facebook_feed
product-image-optimizer photo.jpg -o twitter/ --preset twitter_card
```
Result: Platform-optimized images in seconds.

---

### Developer / Automation
**Problem:** Need to integrate image processing into existing Python workflow.

**Solution:**
```python
from product_image_optimizer import ImageProcessor, get_preset

def process_new_uploads(upload_dir, output_dir):
    config = get_preset("ecommerce_square")
    processor = ImageProcessor(config)

    for img in upload_dir.glob("*.jpg"):
        out = output_dir / f"{img.stem}.png"
        processor.process_image(img, out)
```

---

## 🎨 GUI Features

The GUI application provides:
- **Drag & Drop** - Drop files directly into the app
- **Preset Selection** - Choose from platform-specific presets
- **Custom Settings** - Fine-tune dimensions and options
- **Real-time Progress** - Visual progress bar and status
- **Theme Support** - Multiple color themes

**GUI Themes:**
- `default` - Blue accent
- `dark_blue` - GitHub-inspired dark theme
- `purple` - Purple accent
- `green` - Green accent
- `orange` - Orange accent
- `red` - Bold red theme
- `minimal_light` - Clean light theme

Launch with theme:
```python
from product_image_optimizer import launch_gui
launch_gui(theme_name="dark_blue")
```

---

## ⚙️ Technical Details

### Processing Pipeline

1. **Load Image** - PIL/Pillow high-quality loading
2. **Background Removal** - U²-Net AI model (rembg)
3. **Auto-Crop** - Detect product bounds with configurable padding
4. **Intelligent Resize**:
   - Calculate optimal size to fill canvas (configurable ratio)
   - Maintain aspect ratio
   - Ensure minimum dimensions
   - High-quality LANCZOS resampling
5. **Center on Canvas** - Professional product-focused composition
6. **Optimize Output** - PNG compression and optimization

### Performance

- **Speed**: ~2-3 seconds per image (depends on input size and hardware)
- **Quality**: LANCZOS resampling for maximum quality
- **Memory**: Efficient batch processing with ~200MB peak for typical images
- **Scalability**: Tested with batches of 1000+ images

### Dependencies

- **Pillow** (10.0.0+) - Image processing
- **rembg** (2.0.50+) - AI background removal
- **numpy** (1.24.0+) - Numerical operations
- **tkinterdnd2** (0.3.0+) - Optional, for drag & drop GUI

---

## 🧪 Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=product_image_optimizer

# Specific test
pytest tests/test_processor.py
```

---

## 🛠️ Development

### Setup Development Environment

```bash
git clone https://github.com/matte1782/product-image-optimizer.git
cd product-image-optimizer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Code Style

```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/
```

---

## 📊 Benchmarks

Performance on standard hardware (Intel i5, 16GB RAM):

| Image Size | Processing Time | Output Size |
|-----------|----------------|-------------|
| 1000x1000 | ~1.5s | ~150KB |
| 3000x3000 | ~2.5s | ~400KB |
| 6000x6000 | ~4.0s | ~800KB |

*Times include background removal, resize, and PNG optimization.*

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **rembg** - AI background removal
- **Pillow** - Python Imaging Library
- **U²-Net** - Deep learning model for salient object detection

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/matte1782/product-image-optimizer/issues)
- **Documentation**: [README](https://github.com/matte1782/product-image-optimizer#readme)
- **Author**: Matteo Panzeri (University of Pavia, BSX)

---

**Made with ❤️ by Matteo Panzeri for developers, designers, and e-commerce professionals**
