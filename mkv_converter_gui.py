import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import shutil
from pathlib import Path

VERSION = "1.1"


def convert_folder(folder_path: str) -> None:
    """Remux non-MKV files in folder to MKV using FFmpeg."""
    source_dir = Path(folder_path)
    temp_dir = source_dir / "temp"
    temp_dir.mkdir(exist_ok=True)

    for file_path in source_dir.iterdir():
        if file_path.is_dir() or file_path.suffix.lower() == ".mkv":
            continue

        temp_output = temp_dir / (file_path.stem + ".mkv")
        subprocess.run(
            ["ffmpeg", "-i", str(file_path), "-c", "copy", str(temp_output)],
            check=True,
        )

        shutil.move(str(temp_output), source_dir / temp_output.name)
        file_path.unlink()

    try:
        temp_dir.rmdir()
    except OSError:
        messagebox.showinfo("Info", "Temp directory not empty; remove manually if desired.")


def select_folder() -> None:
    path = filedialog.askdirectory(title="Select Source Folder")
    if path:
        folder_var.set(path)
        if messagebox.askyesno("Confirm", f"Convert files in:\n{path}?"):
            convert_folder(path)
            messagebox.showinfo("Done", "Conversion complete!")


# --- GUI setup ---
root = tk.Tk()
root.title(f"MKV Converter v{VERSION}")
root.geometry("500x500")
root.resizable(False, False)

folder_var = tk.StringVar(value="No folder selected")

title_label = tk.Label(root, text=f"MKV Converter v{VERSION}", font=("Arial", 16))
title_label.pack(pady=20)

select_button = tk.Button(root, text="Select Folder & Convert", command=select_folder, width=30)
select_button.pack(pady=10)

folder_label = tk.Label(root, textvariable=folder_var, wraplength=480, justify="left")
folder_label.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit, width=15)
exit_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

root.mainloop()
