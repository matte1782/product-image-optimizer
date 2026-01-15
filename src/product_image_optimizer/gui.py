"""
Modern GUI for Product Image Optimizer.

Features:
- Drag & drop support
- Preset selection
- Theme customization
- Real-time progress tracking
- Batch processing
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
from pathlib import Path
from datetime import datetime
import zipfile
from typing import List, Optional

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD

    HAS_DND = True
except ImportError:
    HAS_DND = False
    print("Warning: tkinterdnd2 not available. Drag & drop disabled.")

from .config import ProcessingConfig, GUITheme
from .processor import ImageProcessor
from .presets import PROCESSING_PRESETS, GUI_THEMES, list_presets


class ProductImageOptimizerGUI:
    """Main GUI application."""

    def __init__(self, root, theme: Optional[GUITheme] = None):
        """
        Initialize GUI.

        Args:
            root: Tkinter root window
            theme: GUI theme. Uses default if not provided.
        """
        self.root = root
        self.theme = theme or GUI_THEMES["default"]
        self.config = ProcessingConfig()
        self.processor = ImageProcessor(self.config)

        self.processing_queue = queue.Queue()
        self.is_processing = False
        self.image_files = []

        self.setup_window()
        self.create_ui()

    def setup_window(self):
        """Configure main window."""
        self.root.title("Product Image Optimizer")
        self.root.geometry("900x750")
        self.root.configure(bg=self.theme.dark)
        self.root.resizable(False, False)

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f"900x750+{x}+{y}")

    def create_ui(self):
        """Create user interface."""

        # ===== HEADER =====
        header = tk.Frame(self.root, bg=self.theme.primary, height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="PRODUCT IMAGE OPTIMIZER",
            font=("Segoe UI", 24, "bold"),
            bg=self.theme.primary,
            fg=self.theme.text,
        )
        title.pack(pady=(20, 5))

        subtitle = tk.Label(
            header,
            text="Professional image processing for e-commerce and social media",
            font=("Segoe UI", 10),
            bg=self.theme.primary,
            fg=self.theme.text,
        )
        subtitle.pack()

        # ===== MAIN CONTENT =====
        content = tk.Frame(self.root, bg=self.theme.dark)
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Left panel: Controls
        left_panel = tk.Frame(content, bg=self.theme.surface, width=380)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_panel.pack_propagate(False)

        self.create_control_panel(left_panel)

        # Right panel: Drop zone and progress
        right_panel = tk.Frame(content, bg=self.theme.dark)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_drop_zone(right_panel)
        self.create_progress_panel(right_panel)

    def create_control_panel(self, parent):
        """Create control panel with presets and settings."""

        # Preset selection
        preset_frame = tk.Frame(parent, bg=self.theme.surface)
        preset_frame.pack(fill=tk.X, padx=20, pady=20)

        preset_label = tk.Label(
            preset_frame,
            text="⚙️ Preset Configuration",
            font=("Segoe UI", 11, "bold"),
            bg=self.theme.surface,
            fg=self.theme.text,
        )
        preset_label.pack(anchor=tk.W, pady=(0, 10))

        self.preset_var = tk.StringVar(value="ecommerce_square")

        preset_options = list_presets()
        for preset in preset_options:
            rb = tk.Radiobutton(
                preset_frame,
                text=preset.replace("_", " ").title(),
                variable=self.preset_var,
                value=preset,
                bg=self.theme.surface,
                fg=self.theme.text,
                selectcolor=self.theme.primary,
                activebackground=self.theme.surface,
                activeforeground=self.theme.text,
                font=("Segoe UI", 9),
                command=self.on_preset_changed,
            )
            rb.pack(anchor=tk.W, pady=2)

        # Custom settings
        tk.Frame(parent, bg=self.theme.primary, height=2).pack(fill=tk.X, pady=15)

        settings_frame = tk.Frame(parent, bg=self.theme.surface)
        settings_frame.pack(fill=tk.X, padx=20)

        settings_label = tk.Label(
            settings_frame,
            text="🔧 Custom Settings",
            font=("Segoe UI", 11, "bold"),
            bg=self.theme.surface,
            fg=self.theme.text,
        )
        settings_label.pack(anchor=tk.W, pady=(0, 10))

        # Dimensions
        dim_frame = tk.Frame(settings_frame, bg=self.theme.surface)
        dim_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            dim_frame,
            text="Dimensions:",
            bg=self.theme.surface,
            fg=self.theme.text,
            font=("Segoe UI", 9),
        ).pack(side=tk.LEFT)

        self.width_var = tk.IntVar(value=2000)
        self.height_var = tk.IntVar(value=2000)

        width_entry = tk.Entry(
            dim_frame, textvariable=self.width_var, width=6, font=("Segoe UI", 9)
        )
        width_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(dim_frame, text="x", bg=self.theme.surface, fg=self.theme.text).pack(
            side=tk.LEFT
        )

        height_entry = tk.Entry(
            dim_frame, textvariable=self.height_var, width=6, font=("Segoe UI", 9)
        )
        height_entry.pack(side=tk.LEFT, padx=5)

        # Options
        self.bg_removal_var = tk.BooleanVar(value=True)
        self.auto_crop_var = tk.BooleanVar(value=True)

        tk.Checkbutton(
            settings_frame,
            text="Remove background",
            variable=self.bg_removal_var,
            bg=self.theme.surface,
            fg=self.theme.text,
            selectcolor=self.theme.primary,
            activebackground=self.theme.surface,
            activeforeground=self.theme.text,
            font=("Segoe UI", 9),
        ).pack(anchor=tk.W, pady=3)

        tk.Checkbutton(
            settings_frame,
            text="Auto-crop",
            variable=self.auto_crop_var,
            bg=self.theme.surface,
            fg=self.theme.text,
            selectcolor=self.theme.primary,
            activebackground=self.theme.surface,
            activeforeground=self.theme.text,
            font=("Segoe UI", 9),
        ).pack(anchor=tk.W, pady=3)

        # Process button
        tk.Frame(parent, bg=self.theme.dark, height=20).pack()

        self.process_btn = tk.Button(
            parent,
            text="🚀 PROCESS IMAGES",
            font=("Segoe UI", 12, "bold"),
            bg=self.theme.success,
            fg=self.theme.text,
            activebackground=self.theme.accent,
            activeforeground=self.theme.text,
            relief=tk.FLAT,
            padx=40,
            pady=15,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.start_processing,
        )
        self.process_btn.pack(pady=15)

    def create_drop_zone(self, parent):
        """Create drag & drop zone."""
        if HAS_DND:
            drop_frame = tk.Frame(
                parent,
                bg=self.theme.surface,
                highlightthickness=2,
                highlightbackground=self.theme.primary,
            )
        else:
            drop_frame = tk.Frame(
                parent,
                bg=self.theme.surface,
                highlightthickness=2,
                highlightbackground=self.theme.warning,
            )

        drop_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        icon = tk.Label(
            drop_frame,
            text="📁",
            font=("Segoe UI", 64),
            bg=self.theme.surface,
            fg=self.theme.text,
        )
        icon.pack(pady=(60, 20))

        if HAS_DND:
            label_text = "Drag & drop images here\nor click to select"
        else:
            label_text = "Click to select images\n(drag & drop unavailable)"

        drop_label = tk.Label(
            drop_frame,
            text=label_text,
            font=("Segoe UI", 14),
            bg=self.theme.surface,
            fg=self.theme.text,
            justify=tk.CENTER,
        )
        drop_label.pack()

        formats = tk.Label(
            drop_frame,
            text="Supports: JPG, PNG, ZIP",
            font=("Segoe UI", 10),
            bg=self.theme.surface,
            fg=self.theme.text,
        )
        formats.pack(pady=10)

        self.files_label = tk.Label(
            drop_frame,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg=self.theme.surface,
            fg=self.theme.success,
        )
        self.files_label.pack(pady=10)

        # Enable drag & drop if available
        if HAS_DND:
            drop_frame.drop_target_register(DND_FILES)
            drop_frame.dnd_bind("<<Drop>>", self.on_drop)

        # Click to browse
        drop_frame.bind("<Button-1>", lambda e: self.browse_files())
        icon.bind("<Button-1>", lambda e: self.browse_files())
        drop_label.bind("<Button-1>", lambda e: self.browse_files())

    def create_progress_panel(self, parent):
        """Create progress display panel."""
        self.progress_frame = tk.Frame(parent, bg=self.theme.surface)

        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg=self.theme.surface,
            fg=self.theme.text,
        )
        self.progress_label.pack(pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=self.theme.dark,
            background=self.theme.primary,
            thickness=25,
        )

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            style="Custom.Horizontal.TProgressbar",
            mode="determinate",
            length=450,
        )
        self.progress_bar.pack(pady=10)

        self.status_label = tk.Label(
            self.progress_frame,
            text="",
            font=("Segoe UI", 9),
            bg=self.theme.surface,
            fg=self.theme.text,
        )
        self.status_label.pack(pady=5)

    def on_preset_changed(self):
        """Handle preset selection change."""
        preset_name = self.preset_var.get()
        preset = PROCESSING_PRESETS[preset_name]

        self.width_var.set(preset.target_width)
        self.height_var.set(preset.target_height)
        self.bg_removal_var.set(preset.remove_background)
        self.auto_crop_var.set(preset.auto_crop)

    def on_drop(self, event):
        """Handle dropped files."""
        if HAS_DND:
            files = self.root.tk.splitlist(event.data)
            self.load_files(files)

    def browse_files(self):
        """Browse for files."""
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Images", "*.jpg *.jpeg *.png"),
                ("ZIP files", "*.zip"),
                ("All files", "*.*"),
            ],
        )
        if files:
            self.load_files(files)

    def load_files(self, files):
        """Load and process file list."""
        self.image_files = []

        for file_path in files:
            path = Path(file_path)

            if path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                self.image_files.append(path)
            elif path.suffix.lower() == ".zip":
                extracted = self.extract_zip(path)
                self.image_files.extend(extracted)

        if self.image_files:
            count = len(self.image_files)
            self.files_label.config(
                text=f"✓ {count} image{'s' if count != 1 else ''} loaded"
            )
            self.process_btn.config(state=tk.NORMAL)
        else:
            messagebox.showwarning("No images", "No images found in selected files")

    def extract_zip(self, zip_path: Path) -> List[Path]:
        """Extract ZIP and return image files."""
        import tempfile

        # Use temporary directory
        temp_dir = Path(tempfile.mkdtemp(prefix="product_img_opt_"))

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # Validate ZIP entries to prevent path traversal
                for member in zip_ref.namelist():
                    # Check for path traversal attempts
                    if (
                        member.startswith("/")
                        or ".." in member
                        or member.startswith("\\")
                    ):
                        raise ValueError(f"Unsafe path in ZIP: {member}")

                # Safe to extract
                zip_ref.extractall(temp_dir)

            images = []
            for ext in ["*.jpg", "*.jpeg", "*.png"]:
                images.extend(temp_dir.rglob(ext))

            return images
        except Exception:
            # Clean up on error
            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)
            raise

    def start_processing(self):
        """Start image processing."""
        if self.is_processing:
            return

        # Get output directory
        output_dir = filedialog.askdirectory(title="Choose output directory")
        if not output_dir:
            return

        self.output_dir = Path(output_dir)

        # Update config from UI
        self.config.target_width = self.width_var.get()
        self.config.target_height = self.height_var.get()
        self.config.remove_background = self.bg_removal_var.get()
        self.config.auto_crop = self.auto_crop_var.get()

        # Update processor
        self.processor = ImageProcessor(self.config)

        # Start processing
        self.is_processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.progress_frame.pack(fill=tk.BOTH, expand=True)

        thread = threading.Thread(target=self.process_thread, daemon=True)
        thread.start()
        self.update_progress()

    def process_thread(self):
        """Processing thread."""
        total = len(self.image_files)
        success = 0
        failed = 0

        for i, img_file in enumerate(self.image_files, 1):
            output_file = self.output_dir / f"{img_file.stem}.png"

            ok, error, metadata = self.processor.process_image(img_file, output_file)

            if ok:
                success += 1
            else:
                failed += 1

            self.processing_queue.put(
                {
                    "processed": i,
                    "total": total,
                    "success": success,
                    "failed": failed,
                    "current": img_file.name,
                }
            )

        self.processing_queue.put({"done": True, "output_dir": str(self.output_dir)})

    def update_progress(self):
        """Update progress from queue."""
        try:
            while not self.processing_queue.empty():
                data = self.processing_queue.get_nowait()

                if "done" in data:
                    self.is_processing = False
                    self.progress_bar["value"] = 100
                    self.progress_label.config(text="✅ Complete!")
                    self.status_label.config(
                        text=f"Saved to: {data['output_dir']}", fg=self.theme.success
                    )
                    messagebox.showinfo(
                        "Complete",
                        f"All images processed!\n\nOutput: {data['output_dir']}",
                    )
                    self.process_btn.config(state=tk.NORMAL)
                    return

                progress = (data["processed"] / data["total"]) * 100
                self.progress_bar["value"] = progress
                self.progress_label.config(
                    text=f"Processing {data['processed']}/{data['total']}"
                )
                self.status_label.config(
                    text=f"✓ {data['success']} | ✗ {data['failed']} | 📄 {data['current']}"
                )

        except queue.Empty:
            pass

        if self.is_processing:
            self.root.after(100, self.update_progress)


def launch_gui(theme_name: str = "default"):
    """
    Launch the GUI application.

    Args:
        theme_name: Theme to use (from GUI_THEMES)
    """
    theme = GUI_THEMES.get(theme_name, GUI_THEMES["default"])

    if HAS_DND:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()

    app = ProductImageOptimizerGUI(root, theme)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
