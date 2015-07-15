#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, abort
from flask_cors import CORS

import franck.api as api

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

#@app.errorhandler(Exception)
#def handle_invalid_usage(error):
#    return jsonify({'exception': "exception"}), 400
'''
@app.route("/videos", methods=['GET'])
def videos():
    # get args
    if not request.form or request.form.get('url') is None:
        abort(400)
    command = request.form.get('url')
    
    # parse args and load
    if command.startswith('http://'):
        videos = video.from_urls(get_video_urls(command))
    elif command.startswith("random") or command.startswith("r"):
        videos = video.from_configs(get_random_config(command.split(" ")[-1]))
    else:
        videos = []

    # return a nice result
    pretty = [v.pretty() for v in videos]
    
    return jsonify({'videos': pretty}), 200
'''

@app.route("/video/<path:url>", methods=['GET'])
def video(url):
    # TODO: check args
    return jsonify(api.video(url)), 200

if __name__ == "__main__":
    app.run(debug=True)
