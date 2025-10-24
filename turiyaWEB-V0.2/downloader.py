import shutil
import subprocess
import sys
#check if yt-dlp and ffmpeg is installed or not
programs = ['ffmpeg','yt-dlp']
def ensure_install(programs):
    for program in programs:
        res = shutil.which(program)
        if res:
            print(f"{program} is installed at {res} , ;carry on")
        else:
            subprocess.run([sys.executable,"-m","pip","install",program])
ensure_install(programs)

def start_download(link):
    subprocess.run(['yt-dlp',link,"-P","./downloads"])