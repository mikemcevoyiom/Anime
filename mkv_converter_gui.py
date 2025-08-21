import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import shutil
from pathlib import Path
import re

VERSION = "1.1"


progress_re = re.compile(r"fps=(\S+)\s.*time=(\S+)")


def run_ffmpeg(cmd, file_name: str) -> None:
    """Run FFmpeg command while updating progress label."""
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)
    for line in process.stderr:
        match = progress_re.search(line)
        if match:
            fps, tm = match.group(1), match.group(2)
            status_var.set(f"{file_name} | {fps} fps | {tm}")
            root.update_idletasks()
    ret = process.wait()
    if ret != 0:
        raise subprocess.CalledProcessError(ret, cmd)


def convert_folder(folder_path: str) -> None:
    """Remux non-MKV files in folder to MKV using FFmpeg."""
    source_dir = Path(folder_path)
    temp_dir = source_dir / "temp"
    temp_dir.mkdir(exist_ok=True)

    for file_path in source_dir.iterdir():
        if file_path.is_dir() or file_path.suffix.lower() == ".mkv":
            continue

        temp_output = temp_dir / (file_path.stem + ".mkv")
        status_var.set(f"Remuxing {file_path.name}")
        root.update_idletasks()
        run_ffmpeg(["ffmpeg", "-i", str(file_path), "-c", "copy", str(temp_output)], file_path.name)

        shutil.move(str(temp_output), source_dir / temp_output.name)
        file_path.unlink()

    try:
        temp_dir.rmdir()
    except OSError:
        messagebox.showinfo("Info", "Temp directory not empty; remove manually if desired.")
    status_var.set("Done")


def convert_folder_hevc(folder_path: str) -> None:
    """Convert all video files in folder to HEVC codec using FFmpeg."""
    source_dir = Path(folder_path)
    temp_dir = source_dir / "temp"
    temp_dir.mkdir(exist_ok=True)

    for file_path in source_dir.iterdir():
        if file_path.is_dir():
            continue

        try:
            codec = (
                subprocess.run(
                    [
                        "ffprobe",
                        "-v",
                        "error",
                        "-select_streams",
                        "v:0",
                        "-show_entries",
                        "stream=codec_name",
                        "-of",
                        "default=noprint_wrappers=1:nokey=1",
                        str(file_path),
                    ],
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout.strip().lower()
            )
        except subprocess.CalledProcessError:
            continue

        if codec in {"hevc", "h265"}:
            continue

        bitrate_proc = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=bit_rate",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(file_path),
            ],
            capture_output=True,
            text=True,
        )
        bitrate = bitrate_proc.stdout.strip()

        temp_input = temp_dir / file_path.name
        shutil.move(str(file_path), temp_input)

        status_var.set(f"Converting {file_path.name}")
        root.update_idletasks()

        cmd = ["ffmpeg", "-hwaccel", "auto", "-i", str(temp_input), "-c:v", "hevc_amf"]
        if bitrate.isdigit():
            cmd.extend(["-b:v", bitrate])
        cmd.extend(["-c:a", "copy", str(file_path)])
        run_ffmpeg(cmd, file_path.name)

        temp_input.unlink()

    try:
        temp_dir.rmdir()
    except OSError:
        messagebox.showinfo("Info", "Temp directory not empty; remove manually if desired.")
    status_var.set("Done")


def select_folder() -> None:
    path = filedialog.askdirectory(title="Select Source Folder")
    if path:
        folder_var.set(path)
        if messagebox.askyesno("Confirm", f"Convert files in:\n{path}?"):
            convert_folder(path)
            messagebox.showinfo("Done", "Conversion complete!")


def select_folder_hevc() -> None:
    path = filedialog.askdirectory(title="Select Source Folder")
    if path:
        folder_var.set(path)
        if messagebox.askyesno("Confirm", f"Convert to HEVC in:\n{path}?"):
            convert_folder_hevc(path)
            messagebox.showinfo("Done", "HEVC conversion complete!")


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

hevc_button = tk.Button(root, text="Select Folder & Update to HEVC", command=select_folder_hevc, width=30)
hevc_button.pack(pady=10)

folder_label = tk.Label(root, textvariable=folder_var, wraplength=480, justify="left")
folder_label.pack(pady=10)

status_var = tk.StringVar(value="")
status_label = tk.Label(root, textvariable=status_var, wraplength=480, justify="left")
status_label.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=root.quit, width=15)
exit_button.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

root.mainloop()
