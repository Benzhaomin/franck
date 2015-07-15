#!/usr/bin/python
# -*- coding: utf-8 -*-

import franck.utils.parser as parser

class Video:
  
  def __init__(self, url):
    self.url = url
    self.json = None
    
  def load(self):
    if self.json:
      return self
    
    config = parser.video_config(self.url)
    info = parser.video_info(self.url)
    
    self.json = self.beautify(config, info)
  
  def beautify(self, config, info):
    if not config or not info:
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
    }
