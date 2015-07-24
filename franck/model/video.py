#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('franck.logger')

import franck.parser as parser

class Video:
  
  def __init__(self, url):
    self.url = url
    self.json = None
  
  # use self.url for identity
  def __eq__(self, other):
    return isinstance(other, Video) and self.url == other.url
  
  def __ne__(self, other):
    return not self == other
  
  # loads details about the video in a dict
  def load(self):
    if self.json:
      return self
    
    # get data from the player's config xml file
    config = parser.video_config(self.url)
    
    # get data from the video's page
    info = parser.video_info(self.url)
    
    # merge that in a dict
    self.json = self.beautify(config, info)
  
    return self

  # merges data coming from a config file and a page into a dict
  def beautify(self, config, info):
    if not config or not info:
      logger.warning("[video] video data not found at %s", self.url)
      return {}
    
    video_id = config["tracks"][0]["file"].split("=")[-1]
    
    return {
      'id': video_id,
      'url': config["sharing"]["link"],
      'title': info['title'],
      'cover': info['thumbnail'],
      'sources': { item["label"]: {'file': item["file"], 'size': 0} for item in config["sources"]},
      'iframe':  'http://www.jeuxvideo.com/videos/iframe/' + video_id,
      'description': info['description'],
      'timeline': info['thumbnail'].replace('high.jpg', '0000.jpg'),
    }
  
  # returns a source dict {'file': url, 'size':0}
  def get_source(self, quality='1080p'):
    # json must be loaded
    if not self.json:
      logger.debug("[video] tried to get a source on an unloaded video")
      return None
    
    sources = self.json['sources']
    
    # try to get the requested quality
    if quality in sources:
      return sources[quality]
    
    # otherwise just get the best we can find
    return self.get_source(self.get_best_quality())

  # returns the best quality available, as a string
  def get_best_quality(self):
    # json must be loaded
    if not self.json:
      logger.debug("[video] tried to get the best quality on an unloaded video")
      return None
    
    sources = self.json['sources']
    
    for quality in ['1080p', '720p', '400p', '272p']:
      if quality in sources:
        return quality
    
    logger.warning("[video] found a loaded video with no source file %s", self.url)
    return None
