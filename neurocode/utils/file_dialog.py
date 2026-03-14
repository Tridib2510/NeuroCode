from tkinter import Tk
from tkinter.filedialog import askopenfilename
from typing import Optional
import sys


def select_image_file(
    title: str = "Select Image", initialdir: Optional[str] = None
) -> str:
    """
    Opens a file dialog to select an image file.

    Args:
        title (str): The title of the file dialog window. Defaults to "Select Image".
        initialdir (str): The initial directory to open the dialog in. Defaults to None.

    Returns:
        str: The path to the selected image file, or an empty string if cancelled.
    """
    try:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        root.update()

        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.webp"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*"),
        ]

        file_path = askopenfilename(
            title=title, initialdir=initialdir, filetypes=filetypes
        )

        root.destroy()

        return file_path
    except Exception as e:
        print(f"Error opening file dialog: {e}", file=sys.stderr)
        return ""
