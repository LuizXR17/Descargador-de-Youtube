from flask import Flask, request, send_file, render_template
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        download_type = request.form.get('download_type')

        if 'youtube.com' not in url:
            return 'URL inválida. Por favor, ingrese una URL de YouTube.'

        yt = YouTube(url)

        download_path = os.path.join(os.getcwd(), 'descargas')

        if not os.path.exists(download_path):
            os.makedirs(download_path)

        if download_type == 'audio':
            stream = yt.streams.get_audio_only()
            filename = stream.download(download_path)
        else:
            stream = yt.streams.get_highest_resolution()
            filename = stream.download(download_path)

        return send_file(filename, as_attachment=True)
    else:
        return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)