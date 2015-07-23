#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import logging

logger = logging.getLogger('franck.logger')

from bottle import get, run

import franck.api as api

@get("/videos/<url:path>")
# curl http://localhost:8080/videos/http://www.jeuxvideo.com/toutes-les-videos/type-7340/machine-40/genre-2050/
def videos(url):
    # TODO: check args
    
    videos_info = api.videos(url)
    
    if len(videos_info) == 0:
        video_info = api.video(url)
        
        if len(video_info) > 0:
            videos_info = [video_info]
    
    return {'videos': videos_info}
    
@get("/video/<url:path>")
# curl http://localhost:8080/video/http://www.jeuxvideo.com/videos/gaming-live/433637/rocket-league-du-foot-motorise-a-l-essai-en-split-screen.htm
def video(url):
    # TODO: check args
    
    video_info = api.video(url)
    
    return video_info
    
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
    run(host='localhost', port=8080, debug=True)
    
