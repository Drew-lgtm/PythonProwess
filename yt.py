import tkinter as tk
import os
import subprocess
import threading
from tkinter import messagebox

def download_video():
    url = url_entry.get().strip()
    if "youtube.com" not in url and "youtu.be" not in url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL")
        return

    download_path = os.path.expanduser("~/Downloads/mp3")
    os.makedirs(download_path, exist_ok=True)

    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", os.path.join(download_path, "%(title).100s.%(ext)s"),
        url,
    ]

    download_button.config(state="disabled", text="Downloading...")
    threading.Thread(target=run_download, args=(command, download_path), daemon=True).start()

def run_download(command, download_path):
    try:
        subprocess.run(command, check=True)
        root.after(0, on_download_done, True, f"Download completed.\nSaved to: {download_path}")
    except FileNotFoundError:
        root.after(0, on_download_done, False, "yt-dlp is not installed or not on PATH.\nInstall it with: pip install yt-dlp")
    except subprocess.CalledProcessError as e:
        root.after(0, on_download_done, False, f"Download failed:\n{e}")

def on_download_done(success, message):
    download_button.config(state="normal", text="Download MP3")
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

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
