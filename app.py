import os
import subprocess
from flask import Flask, request, render_template, send_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'videoFile' not in request.files:
        return 'No video file uploaded'

    video_file = request.files['videoFile']

    if video_file.filename == '':
        return 'No selected video file'

    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
    audio_path = os.path.splitext(video_path)[0] + '.mp3'

    # Save the video file to the uploads folder
    video_file.save(video_path)

    # Convert video to MP3
    convert_video_to_mp3(video_path, audio_path)

    # Provide download link for the converted MP3 file
    return f'Video file uploaded and <a href="/download/{os.path.basename(audio_path)}">converted to MP3</a> successfully!'

@app.route('/download/<filename>')
def download(filename):
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(audio_path):
        return 'File not found'

    return send_file(audio_path, as_attachment=True)

def convert_video_to_mp3(input_file, output_file):
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        "-ar", "44100",
        "-y",
        output_file
    ]
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print("Conversion succeeded")
    except subprocess.CalledProcessError as e:
        print("Conversion failed")

if __name__ == '__main__':
    app.run(debug=True)
