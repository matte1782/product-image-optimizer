# Examples

This directory contains example usage and before/after comparisons.

## Directory Structure

```
examples/
├── input/          # Example input images
├── output/         # Processed output images
└── README.md       # This file
```

## Usage

1. Place your test images in the `input/` directory
2. Run the CLI:
   ```bash
   product-image-optimizer examples/input/ -o examples/output/ --preset ecommerce_square
   ```
3. Check the results in `output/`

## Example Commands

### E-commerce (Square)
```bash
product-image-optimizer examples/input/ -o examples/output/ecommerce/ --preset ecommerce_square
```

### Instagram (Square)
```bash
product-image-optimizer examples/input/ -o examples/output/instagram/ --preset instagram_square
```

### Custom Dimensions
```bash
product-image-optimizer examples/input/ -o examples/output/custom/ -w 1500 -h 2000
```

### No Background Removal
```bash
product-image-optimizer examples/input/ -o examples/output/no-bg/ --no-bg-removal
```

## Notes

- Add your own images to the `input/` directory to test
- The `output/` directory is gitignored to avoid committing large files
- For best results, use high-quality source images (2000px+ width)
