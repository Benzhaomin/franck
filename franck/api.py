#!/usr/bin/python
# -*- coding: utf-8 -*-

import franck.utils.parser as parser
import franck.utils.crawler as crawler

from franck.model.video import Video

# get all the videos found on a page
def videos(url):
  pages = parser.video_pages(url)
  
  return [video(url) for url in pages]
  
# get the video config info of a single page or all sub-pages of a section
def video(url):
  v = Video(url)
  v.load()
  return v.json
