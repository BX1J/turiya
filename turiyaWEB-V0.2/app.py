from flask import Flask, render_template, request
from downloader import start_download
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/download',methods=['POST'])
def download():
    link = request.get_json()
    link = link['link']
    download1 = threading.Thread(target=start_download(link))
    return {"status":"downloading"}
    



if __name__ == "__main__":
    app.run(port=5000,debug=True)