import os
import time

from flask import Flask, render_template, Response, request, jsonify

from opencv import get_frames
from redis_db import get_classes as r_get_classes

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['video']

    filename = f"{int(time.time())}_{file.filename}"
    file.save(os.path.join('uploads', filename))

    return filename


@app.route('/video_feed')
def video_feed():
    return Response(
        get_frames(request.args.get('filename')),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/get_classes')
def get_classes():
    return jsonify(r_get_classes(request.args.get('filename')))


if __name__ == '__main__':
    app.run(debug=True)

