import argparse
from urllib.parse import urlparse
import subprocess
import os

# Ask the user for cli argument
parser = argparse.ArgumentParser(description="Turiya Downloader")
parser.add_argument("query",help="The URL or search term to download!")
parser.add_argument("--path", help="Custom download folder (optional)")
args = parser.parse_args()
UserDefinedPath = args.path
print(UserDefinedPath)

# Check if the user input is a link or a search term.
result = urlparse(args.query)
if result.scheme and result.netloc:
    url = args.query
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    os.makedirs(os.path.join(downloads_path, "Turiya"), exist_ok=True)

    try:
        subprocess.run(["yt-dlp", "-o", f"{downloads_path}/%(title)s.%(ext)s", url], check=True)
        print("Download in progress...")
    except subprocess.CalledProcessError as e:
        print("❌ Download failed. Please check the URL or your connection.")

else:
    print("Search not yet supported!")
