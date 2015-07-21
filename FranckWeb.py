#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging

logger = logging.getLogger('franck.logger')

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

@app.route("/videos/<path:url>", methods=['GET'])
# curl http://localhost:5000/videos/http://www.jeuxvideo.com/toutes-les-videos/type-7340/machine-40/genre-2050/
def videos(url):
    # TODO: check args
    
    videos_info = api.videos(url)
    if len(videos_info) == 0:
        videos_info = [api.video(url)]
    
    return jsonify({'videos': videos_info}), 200
    
@app.route("/video/<path:url>", methods=['GET'])
# curl http://localhost:5000/video/http://www.jeuxvideo.com/videos/gaming-live/433637/rocket-league-du-foot-motorise-a-l-essai-en-split-screen.htm
def video(url):
    # TODO: check args
    
    video_info = api.video(url)
    
    return jsonify(video_info), 200
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', dest='loglevel', default='WARNING')
    args = parser.parse_args()
    
    # set logger level
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    
    logging.basicConfig(level=numeric_level, format='%(asctime)s %(message)s')
    
    # gogogo
    app.run() #debug=args.verbose
    
