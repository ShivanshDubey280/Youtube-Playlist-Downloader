import os
import re
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from pytubefix import Playlist, YouTube
from tenacity import retry, stop_after_attempt, wait_fixed
import threading

# Function to sanitize filenames
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '-', filename)

# Function to download playlist with resolution selection
def download_playlist_gui():
    playlist_url = url_entry.get()
    resolution = resolution_var.get()

    if not playlist_url:
        messagebox.showerror("Error", "Please enter a playlist URL")
        return
    
    download_directory = filedialog.askdirectory()
    if not download_directory:
        return

    # Disable the download button while downloading
    download_btn.config(state=tk.DISABLED)
    
    # Run download process in a separate thread to avoid freezing the GUI
    threading.Thread(target=download_playlist, args=(playlist_url, resolution, download_directory)).start()

def download_playlist(playlist_url, resolution, download_directory):
    try:
        playlist = Playlist(playlist_url)
        playlist_name = sanitize_filename(re.sub(r'\W+', '-', playlist.title))
        playlist_path = os.path.join(download_directory, playlist_name)
        
        if not os.path.exists(playlist_path):
            os.mkdir(playlist_path)

        total_videos = len(playlist.videos)
        progress_bar["maximum"] = total_videos

        for index, video in enumerate(playlist.videos, start=1):
            yt = YouTube(video.watch_url, on_progress_callback=progress_function)
            video_streams = yt.streams.filter(res=resolution)

            video_filename = sanitize_filename(f"{index}. {yt.title}.mp4")
            video_path = os.path.join(playlist_path, video_filename)

            if os.path.exists(video_path):
                update_status(f"{video_filename} already exists, skipping...")
                continue

            if not video_streams:
                highest_resolution_stream = yt.streams.get_highest_resolution()
                update_status(f"Downloading {yt.title} in {highest_resolution_stream.resolution}")
                download_with_retries(highest_resolution_stream, video_path)
            else:
                video_stream = video_streams.first()
                update_status(f"Downloading video for {yt.title} in {resolution}")
                download_with_retries(video_stream, "video.mp4")

                audio_stream = yt.streams.get_audio_only()
                update_status(f"Downloading audio for {yt.title}")
                download_with_retries(audio_stream, "audio.mp4")

                # Merging video and audio
                if os.path.exists("video.mp4") and os.path.exists("audio.mp4"):
                    update_status(f"Merging video and audio for {yt.title}")
                    os.system("ffmpeg -y -i video.mp4 -i audio.mp4 -c:v copy -c:a aac final.mp4 -loglevel quiet -stats")
                    if os.path.exists("final.mp4"):
                        os.rename("final.mp4", video_path)
                        os.remove("video.mp4")
                        os.remove("audio.mp4")
                else:
                    update_status("Failed to download video or audio.")

            # Update progress bar and percentage
            progress_bar["value"] = index
            percentage = (index / total_videos) * 100
            progress_lbl.config(text=f"Overall Progress: {percentage:.2f}% complete", anchor="w")
            root.update_idletasks()

        update_status("Playlist download completed!")
        messagebox.showinfo("Success", "Playlist downloaded successfully!")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    
    finally:
        download_btn.config(state=tk.NORMAL)

@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def download_with_retries(stream, filename):
    stream.download(filename=filename)

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_lbl.config(text=f"Video Download: {percentage_of_completion:.2f}% complete", anchor="w")

def update_status(status_message):
    status_lbl.config(text=status_message)
    root.update_idletasks()

# Setting up the GUI
root = tk.Tk()
root.title("YouTube Playlist Downloader")
root.geometry("500x300")

# URL Label and Entry
tk.Label(root, text="Playlist URL:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Resolution Selection Label
tk.Label(root, text="Resolution:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
resolution_var = tk.StringVar(value="720p")
resolutions = ["240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
resolution_menu = tk.OptionMenu(root, resolution_var, *resolutions)
resolution_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Status Label
status_lbl = tk.Label(root, text="Waiting to start download...", anchor="w")
status_lbl.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Progress percentage Label
progress_lbl = tk.Label(root, text="", anchor="w")
progress_lbl.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Download Button
download_btn = tk.Button(root, text="Download", command=download_playlist_gui)
download_btn.grid(row=5, column=0, columnspan=2, pady=20)

# Run the application
root.mainloop()