# YouTube Playlist Downloader

A Python-based tool that allows you to download videos from a YouTube playlist in your desired resolution, merging video and audio streams using `ffmpeg`. The tool supports downloading full playlists and selecting the resolution for each video.

## Features

- Download entire YouTube playlists.
- Choose video resolution (240p, 360p, 480p, 720p, 1080p, 1440p, 2160p).
- Automatically merges video and audio streams using `ffmpeg`.
- Progress bar for download status using `tqdm`.

## Requirements

- Python 3.7 or higher
- `ffmpeg` installed on your system (instructions below).
- Required Python libraries: `pytubefix`, `tqdm`, `tenacity`.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/youtube-playlist-downloader.git
cd youtube-playlist-downloader
```
### 2. Install Python dependencies
You can install the required Python libraries using pip. Run the following command:
```bash
pip install pytubefix tqdm tenacity
sudo apt-get install python3-tk
pip install pytubefix
```
### 3. Install FFmpeg
#### Windows:
- Download ffmpeg from FFmpeg official site.
- Extract the downloaded archive.
- Add the bin folder (e.g., C:\ffmpeg\bin) to your system's PATH:
- Right-click This PC → Properties → Advanced system settings → Environment Variables.
- Under System variables, select Path, and click Edit.
- Click New and paste the path to the bin folder.
- Restart your terminal to apply changes.

#### macOS:
```bash
brew install ffmpeg
```
#### Linux (Ubuntu):
```bash
sudo apt update
sudo apt install ffmpeg
```
### 4. Run the Script
To download a playlist, simply run:
```
bash
python download.py
```
- You'll be prompted to enter the playlist URL.
- Choose a resolution from the available options.
- The videos will be downloaded into a folder named after the playlist.
Usage Example
```bash
Enter the playlist url: https://youtube.com/playlist?list=YOUR_PLAYLIST_ID
Please select a resolution ['240p', '360p', '480p', '720p', '1080p', '1440p', '2160p']: 720p
Downloading playlist: 100% [=========================] 11/11
```

## Leave a STAR⭐ nd FOLLOW!🫂
