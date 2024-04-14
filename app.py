from flask import Flask, render_template, request
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    video_quality = request.form['quality']
    
    try:
        youtube = YouTube(video_url)
        
        if video_quality == "HD":
            # For HD, choose the highest resolution stream available.
            video_stream = youtube.streams.get_highest_resolution()
        else:
            # For other quality options, use progressive streams.
            video_stream = youtube.streams.filter(progressive=True, file_extension='mp4', res=video_quality).first()
        
        video_stream.download('./downloads')
        file_name = video_stream.default_filename
        return render_template('download.html', file_name=file_name)
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
