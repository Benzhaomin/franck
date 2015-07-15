#!/usr/bin/python
# -*- coding: utf-8 -*-

import franck.utils.crawler as crawler

from franck.model.video import Video

# get all videos pages in a section (eg, gaming-live, speed game, etc)
def videos(url):
  pages = crawler.crawl(url)
  return pages
  
# get the video config info of a single page or all sub-pages of a section
def video(url):
  v = Video(url)
  v.load()
  return v.json
