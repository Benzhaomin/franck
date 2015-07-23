#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import logging

logger = logging.getLogger('franck.logger')

import franck.api as api

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  
  parser.add_argument('--log', dest='loglevel', default='WARNING',
    help='set the level of messages to display')
  
  parser.add_argument('--quality', dest='quality', default='1080p',
    help='select a video quality 1080p (default), 720p, 400p or 272p')
  
  parser.add_argument('pages', metavar='url', nargs='+',
    help='url of a video or video list page')
  
  args = parser.parse_args()
  
  # set logger level
  numeric_level = getattr(logging, args.loglevel.upper(), None)
  if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
  
  logging.basicConfig(level=numeric_level, format='%(asctime)s %(message)s')
  
  # get quality param
  quality = args.quality
  
  # load requested pages
  for url in args.pages:
    videos = api.videos(url)
    
    if len(videos) == 0:
      videos = api.video(url)
      
      if len(videos) > 0:
        videos = [videos]
  
  # print video files URLs
  for video in videos:
    title = video.json['title']
    source = video.get_source(quality)
    if source:
      url = source['file']
      print(title, url, sep='\t')
      #print('{title} === {url}'.format(title=title, url=url))
    
