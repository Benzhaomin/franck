#!/usr/bin/env python
# -*- coding: utf-8 -*-

from franck.model.video import Video

import os
import unittest
import json

def build_video():
  with open(os.path.join(os.path.dirname(__file__), 'files', 'video_json.json')) as jsondump:
    v = Video('http://www.jeuxvideo.com/gaming-live/0001/00011717/kingdom-hearts-chain-of-memories-gameboy-advance-gba-sora-00000849.htm')
    v.json = json.load(jsondump)
    return v

def get_video_config():
  with open(os.path.join(os.path.dirname(__file__), 'files', 'video_config.json')) as jsondump:
    return json.load(jsondump)
    
def get_video_info():
  with open(os.path.join(os.path.dirname(__file__), 'files', 'video_info.json')) as jsondump:
    return json.load(jsondump)
  
# recursive ordering (dict/list with nested dict/list)
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj
  
class TestVideoGetSource(unittest.TestCase):
    
  # want default (1080p) has 400p max
  def test_get_source_default_quality_auto_select(self):
    v = build_video()
    expected = 'http://videohd.jeuxvideo.com/200705/kingdom_hearts_gba-00000849-high.mp4'
    actual = v.get_source()['file']
    self.assertEqual(actual, expected)
    
  # want something else (272p) has it
  def test_get_source_select_quality_has_it(self):
    v = build_video()
    expected = 'http://video.jeuxvideo.com/200705/kingdom_hearts_gba-00000849-low.mp4'
    actual = v.get_source('272p')['file']
    self.assertEqual(actual, expected)

class TestVideoBeautify(unittest.TestCase):
  def test_beautify(self):
    
    v = Video('http://www.jeuxvideo.com/gaming-live/0001/00011717/kingdom-hearts-chain-of-memories-gameboy-advance-gba-sora-00000849.htm')
    config = get_video_config()
    info = get_video_info()
    
    expected = build_video().json
    actual = v.beautify(config, info)
    
    self.assertEqual(ordered(actual), ordered(expected))
    
if __name__ == '__main__':
  unittest.main()
