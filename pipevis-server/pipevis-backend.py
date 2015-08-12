#!/usr/bin/env python

import json
from flask import Flask, url_for, jsonify, request, Response, send_file, send_from_directory
from core.giphy_api import GiphyApi
from core.pipeline import Pipeline

app = Flask(__name__,static_url_path='/static')
giphy = GiphyApi(
{
"success":["win","dance","success","epic"],
"fail":["fail","failure","wrekt","crying"],
"working":["working","excited"]
}
)
pipeline = Pipeline(giphy)

@app.route('/')
def api_root():
    return app.send_static_file('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('png', path)

@app.route('/pipeline/notify', methods=['POST'])
def pipeline_notify():
    global pipeline
    if not request.json:
        return "Not json format", 406
    pipeline.create_notification(request.json)
    return '',200

@app.route('/pipeline/progress')
def pipeline_step():
    global pipeline
    pipeline.progress()
    return '',200

@app.route('/pipeline/fail')
def pipeline_fail():
    global pipeline
    pipeline.fail()
    return '',200

@app.route('/pipeline/get')
def pipeline_get():
    global pipeline
    if not hasattr(pipeline, 'data'):
        return '{}',200

    pipeline_data = pipeline.data
    pipeline_data['progress'] = pipeline.progress_percentage()
    return json.dumps(pipeline_data)

@app.route('/pipeline/init', methods=['POST'])
def pipeline_init():
    if not request.json:
        return "Not json format", 406
    global pipeline
    pipeline.init_data(request.json)

    return '',200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
