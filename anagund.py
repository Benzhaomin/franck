#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

import franck.model.video as video

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("what page?")
        sys.exit(1)

    video.parse(sys.argv[1])
