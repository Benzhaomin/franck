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

@app.route("/videos/<path:url>", methods=['GET'])
# curl http://localhost:5000/videos/http://www.jeuxvideo.com/toutes-les-videos/type-7340/machine-40/genre-2050/
def videos(url):
    # TODO: check args
    
    videos_info = api.videos(url)
    
    return jsonify({'videos': videos_info}), 200
    
@app.route("/video/<path:url>", methods=['GET'])
# curl http://localhost:5000/video/http://www.jeuxvideo.com/videos/gaming-live/433637/rocket-league-du-foot-motorise-a-l-essai-en-split-screen.htm
def video(url):
    # TODO: check args
    
    video_info = api.video(url)
    
    return jsonify(video_info), 200

if __name__ == "__main__":
    app.run(debug=True)
