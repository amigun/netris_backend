import os
import time

from flask import Flask, render_template, Response, request, jsonify
from flask_cors import CORS, cross_origin

from opencv import get_frames
from redis_db import get_classes as r_get_classes

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
@cross_origin()
def upload():
    file = request.files['video']

    filename = f"{int(time.time())}_{file.filename}"
    file.save(os.path.join('uploads', filename))

    return filename


@app.route('/video_feed')
@cross_origin()
def video_feed():
    return Response(
        get_frames(request.args.get('filename')),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/get_classes')
@cross_origin()
def get_classes():
    return jsonify(r_get_classes(request.args.get('filename')))


if __name__ == '__main__':
    app.run(debug=True)

