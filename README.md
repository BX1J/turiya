# 🎯 Turiya Downloader

Turiya is an **intelligent, command-line downloader** that helps you grab videos, lectures, and media from the web without wasting hours hunting for them.

Built with Python + [yt-dlp](https://github.com/yt-dlp/yt-dlp), it makes downloading content **simple, fast, and organized**.

---

## 🚀 Features (Phase 1)
- Download any supported media by just pasting the URL.
- Automatically saves into your `Downloads/Turiya` folder.
- Friendly CLI messages before/after download.
- Error handling (no ugly crashes).
- (Optional) Custom download path with `--path`.
- (Optional) Keeps a `downloads.log` of what you downloaded.

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/BX1J/turiya.git
cd turiya
```
---
### 2. Install dependencies

Make sure you have Python 3.7+ installed. Then install the required package:
```bash 
pip install -r requirements.txt
```
### 🚀 Usage, Run from command line:
```bash 
python turiya.py "https://www.youtube.com/watch?v=BBJa32lCaaY"
```
This will download the video and save it in `~/Downloads/Turiya/`

### Output file structure:
```bash
Downloads/
└── Turiya/
    ├── VideoTitle.mp4
    └── AnotherVideo.mkv
```
> ⚠️ Note: Always wrap URLs in quotes " " to avoid shell issues.
---
## 🤝 Contributing
Want to improve Turiya? Contributions are welcome!
Fork the repo, make your changes, and open a pull request. Some ideas:
- Add search support
- Build an installer/standalone .exe
- Improve error handling & logging
- Add GUI mode (could really use that)

## 🌟 Support
If you like this project:
- ⭐ Star this repo
- Share with your friends
- Open issues/PRs with suggestions