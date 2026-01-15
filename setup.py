"""Setup configuration for Product Image Optimizer."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="product-image-optimizer",
    version="1.0.0",
    author="Matteo Panzeri",
    author_email="matteo1782@gmail.com",
    description="Professional image processing for e-commerce and social media",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matte1782/product-image-optimizer",
    project_urls={
        "Bug Tracker": "https://github.com/matte1782/product-image-optimizer/issues",
        "Documentation": "https://github.com/matte1782/product-image-optimizer#readme",
        "Source Code": "https://github.com/matte1782/product-image-optimizer",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Graphics :: Editors",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Pillow>=10.0.0",
        "rembg>=2.0.50",
        "numpy>=1.24.0",
    ],
    extras_require={
        "gui": ["tkinterdnd2>=0.3.0"],
        "dev": ["pytest>=7.0.0", "pytest-cov>=4.0.0", "black>=23.0.0", "flake8>=6.0.0"],
        "all": ["tkinterdnd2>=0.3.0", "pytest>=7.0.0", "pytest-cov>=4.0.0"],
    },
    entry_points={
        "console_scripts": [
            "product-image-optimizer=product_image_optimizer.cli:main",
            "product-image-optimizer-gui=product_image_optimizer.gui:launch_gui",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="image processing, background removal, e-commerce, product photography, resize, optimization",
)
