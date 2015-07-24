#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('franck.logger')

import franck.parser as parser

class Video:
  
  def __init__(self, url):
    self.url = url
    self.json = None
  
  def __eq__(self, other):
    return isinstance(other, Video) and self.url == other.url
  
  def load(self):
    if self.json:
      return self
    
    config = parser.video_config(self.url)
    info = parser.video_info(self.url)
    
    self.json = self.beautify(config, info)
  
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
    
    # no quality = no source
    if not quality:
      return None
      
    sources = self.json['sources']
    
    # try to get the requested quality
    if quality in sources:
      return sources[quality]
    
    # otherwise just get the best we can find
    return self.get_source(self._get_best_quality())

  # returns a source dict ['file': url, 'size':0]
  def _get_best_quality(self):
    sources = self.json['sources']
    
    for quality in ['1080p', '720p', '400p', '272p']:
      if quality in sources:
        return quality
    
    logger.warning("[video] found a loaded video with no source file %s", video.url)
    
