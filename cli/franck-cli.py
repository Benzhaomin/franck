#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import franck.model.video as video

DOWNLOAD_DIR='/share/videos/games/'

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    videos = video.parse(" ".join(sys.argv[1:]))
    
    for v in videos:
        print(v.get_download_url() + " -O " + DOWNLOAD_DIR + v.get_filename())
