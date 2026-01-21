<div align="center">
  <h1>🎬 YouTube Auto-Downloader 🎬</h1>
  <p><strong>Hands‑free, clipboard‑based YouTube video & playlist downloader in Python</strong></p>
  <p>Copy a YouTube link → the script queues it → downloads automatically in the best available quality.</p>

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

</div>

---

## 📌 Overview

This project is a **zero‑interaction YouTube downloader** that continuously monitors your system clipboard. Whenever you copy a valid YouTube video, shorts, or playlist URL, it is **automatically queued and downloaded**—no pasting, no commands, no limits.

It is designed to be:

* Fast (multi‑threaded queue)
* Safe (duplicate detection per session)
* Clean (automatic folder organization)
* Informative (colored logs + progress bars)

---

## ✨ Key Features

| Feature                      | Description                                                            |
| ---------------------------- | ---------------------------------------------------------------------- |
| **Clipboard Monitoring**     | Automatically detects YouTube links copied to the clipboard.           |
| **Queue‑Based Downloads**    | Links are added to a download queue and processed safely in order.     |
| **Multi‑Threaded Workers**   | Configurable worker pool for concurrent downloads.                     |
| **Video + Playlist Support** | Handles single videos, Shorts, and full playlists.                     |
| **Highest Resolution**       | Downloads the best available stream automatically.                     |
| **Smart Folder Structure**   | Videos → `downloads/videos`<br>Playlists → `downloads/<playlist_name>` |
| **Duplicate Protection**     | Prevents re‑downloading the same link during a session.                |
| **Live Progress Bars**       | Real‑time progress using `tqdm`.                                       |
| **Colored Logs**             | Clear status messages using `colorama`.                                |

---

## 🧠 How It Works

1. Script starts and initializes folders, queue, and worker threads.
2. Clipboard is checked every second (configurable).
3. A copied URL is:

   * Sanitized
   * Validated (video / shorts / playlist)
   * Added to the download queue
4. Worker threads pick items from the queue:

   * Playlists → downloaded sequentially into their own folder
   * Videos → downloaded into `downloads/videos`
5. Each download shows a live progress bar.

The script runs indefinitely until manually stopped.

---

## 📂 Output Structure

```
downloads/
├── videos/
│   ├── video1.mp4
│   └── video2.mp4
└── Playlist Name/
    ├── track1.mp4
    ├── track2.mp4
    └── track3.mp4
```

---

## ⚙️ Configuration

Modify these constants at the top of the script:

| Variable         | Description                          | Default       |
| ---------------- | ------------------------------------ | ------------- |
| `OUTPUT_DIR`     | Root download directory              | `"downloads"` |
| `CHECK_INTERVAL` | Clipboard polling interval (seconds) | `1`           |
| `MAX_THREADS`    | Max concurrent downloads             | `4`           |

---

## 🛠 Requirements

* **Python 3.8+**
* Internet connection

### Required Libraries

Install all dependencies using pip:

```bash
pip install pytubefix pyperclip tqdm colorama
```

---

## ▶️ Usage

1. **Run the script**

   ```bash
   python downloader.py
   ```

2. **YouTube opens automatically** (non‑blocking)

3. **Copy any YouTube link**

   * Video
   * Shorts
   * Playlist

4. **Watch it download automatically** in your terminal

The script will continue running and accepting new links until you stop it.

---

## 🧪 Supported URL Types

✔ `https://www.youtube.com/watch?v=...`
✔ `https://youtu.be/...`
✔ `https://www.youtube.com/playlist?list=...`
✔ `https://www.youtube.com/shorts/...`

---

## 🚀 Optional: Build Executable

You can bundle this script into a standalone executable using **PyInstaller**.

```bash
pip install pyinstaller
pyinstaller downloader.spec
```

The executable will appear in the `dist/` directory.

> ⚠️ First launch may take a few seconds due to library initialization.

---

## ⚠️ Disclaimer

This project is for **educational and personal use only**.

Downloading content from YouTube may violate its Terms of Service. You are solely responsible for how you use this software. The author assumes **no liability** for misuse or copyright violations.

---

## ⭐ Notes

* This tool has **no hard download limits**
* Designed for **power users & automation lovers**
* Works best when left running in the background

Happy downloading 🎥🚀
