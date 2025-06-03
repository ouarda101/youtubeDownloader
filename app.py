from flask import Flask, request, jsonify
from pytubefix import YouTube
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_video_backend(url):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        highest_res_stream = streams.get_highest_resolution()

        if highest_res_stream:
            filename = highest_res_stream.default_filename
            download_path = os.path.join(DOWNLOAD_FOLDER, filename)

            if os.path.exists(download_path):
                return False, f"Video '{yt.title}' already exists in '{DOWNLOAD_FOLDER}'."

            highest_res_stream.download(output_path=DOWNLOAD_FOLDER)
            return True, f"Video '{yt.title}' downloaded successfully to '{DOWNLOAD_FOLDER}'."
        else:
            return False, "No progressive MP4 streams found for this video."

    except Exception as e:
        return False, f"An error occurred: {e}"

@app.route('/download', methods=['POST'])
def download_route():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    video_url = data['url']
    success, message = download_video_backend(video_url)

    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)