from pytubefix import YouTube, Playlist
import webbrowser
import pyperclip
import time
import threading
import os
from datetime import datetime
from tqdm import tqdm
import re
from colorama import init, Fore, Style
from queue import Queue

# ------------------- INIT -------------------
init(autoreset=True)

# ------------------- CONFIG -------------------
OUTPUT_DIR = "downloads"
CHECK_INTERVAL = 1
MAX_THREADS = 4
# --------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

downloaded_links = set()
download_queue = Queue()  # Queue to store pending downloads
active_downloads = []     # Track active download threads


# ------------------- LOGGER -------------------
def log(message, level="INFO"):
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    colors = {
        "INFO": Fore.CYAN,
        "SUCCESS": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED
    }

    color = colors.get(level, Fore.WHITE)
    print(color + f"[{time_str}] [{level}] {message}")


# ------------------- HELPERS -------------------
def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip() or "Untitled"


def progress_hook(pbar):
    def inner(stream, chunk, bytes_remaining):
        total = stream.filesize
        downloaded = total - bytes_remaining
        pbar.total = total
        pbar.n = downloaded
        pbar.refresh()
    return inner


def is_valid_youtube_url(url):
    """Validate YouTube URLs more robustly"""
    patterns = [
        r'^https?://(www\.)?youtube\.com/watch\?v=[\w-]+(&.*)?$',
        r'^https?://(www\.)?youtube\.com/playlist\?list=[\w-]+(&.*)?$',
        r'^https?://youtu\.be/[\w-]+(\?.*)?$',
        r'^https?://(www\.)?youtube\.com/shorts/[\w-]+(\?.*)?$'
    ]
    
    url = url.strip()
    for pattern in patterns:
        if re.match(pattern, url, re.IGNORECASE):
            return True
    return False


# ------------------- DOWNLOADERS -------------------
def download_video(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()

        folder = os.path.join(OUTPUT_DIR, "videos")
        os.makedirs(folder, exist_ok=True)

        log(f"Downloading video: {yt.title}", "INFO")

        with tqdm(
            total=stream.filesize,
            unit="B",
            unit_scale=True,
            desc=safe_filename(yt.title)[:30],
            colour="green"
        ) as pbar:
            yt.register_on_progress_callback(progress_hook(pbar))
            stream.download(output_path=folder)

        log(f"Download completed: {yt.title}", "SUCCESS")

    except Exception as e:
        log(f"Failed to download {url}: {e}", "ERROR")
    finally:
        # Remove from active downloads when done
        if url in downloaded_links:
            downloaded_links.remove(url)


def download_playlist(playlist_url):
    try:
        playlist = Playlist(playlist_url)

        playlist_title = safe_filename(playlist.title)
        if playlist_title == "Untitled":
            playlist_title = playlist_url.split("list=")[-1]

        folder = os.path.join(OUTPUT_DIR, playlist_title)
        os.makedirs(folder, exist_ok=True)

        log(f"Downloading playlist: {playlist_title}", "INFO")

        for video_url in playlist.video_urls:
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()

            log(f"Downloading: {yt.title}", "INFO")

            with tqdm(
                total=stream.filesize,
                unit="B",
                unit_scale=True,
                desc=safe_filename(yt.title)[:30],
                colour="cyan"
            ) as pbar:
                yt.register_on_progress_callback(progress_hook(pbar))
                stream.download(output_path=folder)

        log("Playlist download complete!", "SUCCESS")

    except Exception as e:
        log(f"Failed to download playlist {playlist_url}: {e}", "ERROR")
    finally:
        # Remove from active downloads when done
        if playlist_url in downloaded_links:
            downloaded_links.remove(playlist_url)


# ------------------- DOWNLOAD WORKER -------------------
def download_worker(worker_id):
    """Worker thread that processes downloads from queue"""
    while True:
        url = download_queue.get()  # Wait for a download task
        
        # Determine if it's a playlist or video
        if "playlist" in url:
            download_playlist(url)
        else:
            download_video(url)
        
        download_queue.task_done()  # Mark task as complete


# ------------------- CLIPBOARD MONITOR -------------------
def monitor_clipboard():
    print(Fore.MAGENTA + Style.BRIGHT + "\n=== YouTube Downloader ===\n")
    print(f"Max concurrent downloads: {MAX_THREADS}")
    print("Copy YouTube links to queue them for download")
    print("All links will be downloaded, no limits!\n")

    # Open YouTube without blocking startup
    threading.Thread(
        target=lambda: webbrowser.open("https://www.youtube.com/"),
        daemon=True
    ).start()

    # Start worker threads silently
    for i in range(MAX_THREADS):
        worker = threading.Thread(
            target=download_worker, 
            args=(i+1,), 
            daemon=True
        )
        worker.start()
        active_downloads.append(worker)

    pyperclip.copy("")
    log("Clipboard monitor started. Copy YouTube links to download.", "INFO")

    while True:
        link = pyperclip.paste().strip()

        if is_valid_youtube_url(link) and link not in downloaded_links:
            # Add to queue
            downloaded_links.add(link)
            download_queue.put(link)
            pyperclip.copy("")  # Clear clipboard
            
            queue_size = download_queue.qsize()
            log(f"Added to queue: {link[:80]}... (Queue size: {queue_size})", "INFO")

        time.sleep(CHECK_INTERVAL)


# ------------------- MAIN -------------------
if __name__ == "__main__":
    monitor_clipboard()