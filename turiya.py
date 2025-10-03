import argparse
from urllib.parse import urlparse
import subprocess
import os

# Ask the user for cli argument
parser = argparse.ArgumentParser(description="Turiya Downloader")
parser.add_argument("query",help="The URL or search term to download!")
args = parser.parse_args()
print(f"User Entered: {args.query}")

# Check if the user input is a link or a search term.
result = urlparse(args.query)
if result.scheme and result.netloc:
    url = args.query
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    subprocess.run(["yt-dlp", "-o", f"{downloads_path}/Turiya/%(title)s.%(ext)s", url])

else:
    print("Search not yet supported!")
