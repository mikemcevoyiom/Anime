# MKV Converter

This project provides tools for processing video files with FFmpeg. It can remux non-MKV files into the Matroska (MKV) container without re-encoding and offers an option to update video streams to the HEVC codec while preserving original audio and bit rate when possible. During conversion the GUI displays the active file along with FFmpeg's reported FPS and timestamp, and HEVC updates leverage AMD GPUs through FFmpeg's `hevc_amf` encoder when available. Converted files are temporarily stored in a `temp` subdirectory and moved back to the original folder, leaving only processed files in the source directory.

## Usage

1. Install [FFmpeg](https://ffmpeg.org/) and ensure it is available on your system PATH.
2. Adjust the Python script's `source_dir` to point at the folder you wish to process (e.g., `D:\\Video\\unprocessed\\porn` on Windows).
3. Run the script. It creates a `temp` directory inside the source folder, remuxes files to MKV, then moves them back and deletes the originals.
4. If the `temp` directory is empty after processing, it is removed automatically.

## Requirements

- Python 3
- FFmpeg

Ensure you back up important files before running the script.
