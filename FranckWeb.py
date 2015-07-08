#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, abort
from flask_cors import CORS

import franck.model.video as video

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

#@app.errorhandler(Exception)
#def handle_invalid_usage(error):
#    return jsonify({'exception': "exception"}), 400
    
@app.route("/", methods=['POST'])
def franck():
    # get args
    if not request.form or request.form.get('url') is None:
        abort(400)
    command = request.form.get('url')
    
    # parse args and load
    videos = video.parse(command)
    
    # return a nice result
    pretty = [v.pretty() for v in videos]
    
    return jsonify({'videos': pretty}), 200

if __name__ == "__main__":
    app.run(debug=True)
