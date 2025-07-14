import tkinter as tk
import os
import subprocess
from tkinter import messagebox

def download_video():
    url = url_entry.get().strip()
    if "youtu" not in url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL")
        return

    try:
        # Create download directory
        download_path = os.path.expanduser("~/Downloads/mp3")
        os.makedirs(download_path, exist_ok=True)

        # yt-dlp command with playlist + mp3
        command = [
            "yt-dlp",
            "--extract-audio",
            "--audio-format", "mp3",
            "--yes-playlist",
            "-o", os.path.join(download_path, "%(title).100s.%(ext)s"),
            url
        ]

        subprocess.run(command, check=True)

        messagebox.showinfo("Success", f"Download completed.\nSaved to: {download_path}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Download failed:\n{e}")

# GUI setup
root = tk.Tk()
root.title("YouTube MP3 Downloader")
root.geometry("460x220")
root.configure(bg="#E6E6FA")  # Light violet

# Container frame for layout
frame = tk.Frame(root, bg="#E6E6FA")
frame.pack(padx=20, pady=20, fill="both", expand=True)

label = tk.Label(frame, text="Enter YouTube Video or Playlist URL:", bg="#E6E6FA", fg="#4B0082", font=("Arial", 12))
label.pack(anchor="w", pady=(0, 8))

url_entry = tk.Entry(frame, font=("Arial", 11))
url_entry.pack(fill="x", padx=10, ipady=4)

download_button = tk.Button(frame, text="Download MP3", command=download_video,
                            bg="#8A2BE2", fg="white", font=("Arial", 11), relief="raised", padx=10, pady=5)
download_button.pack(pady=20)

root.mainloop()
