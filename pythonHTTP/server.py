import time
import testAPI

from flask import Flask, render_template, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

path = os.path.abspath("")

UPLOAD_FOLDER = path + '/uploads'
print(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route('/hello')
def hello():
    time.sleep(10)
    return {'hello': 'world'}


@app.post('/upload')
def upload():
    print(request.remote_addr)
    file = request.files['file']
    print(request.files)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    output = testAPI.main(path + '/uploads/' + file.filename)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    response = jsonify({'message': output})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
