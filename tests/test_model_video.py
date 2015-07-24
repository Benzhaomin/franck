#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
from unittest.mock import patch, mock_open

from franck.model.video import Video

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
  
# franck.model.video.Video.get_source()
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

# franck.model.video.Video.beautify()
class TestVideoBeautify(unittest.TestCase):
  
  # check that beautify correctly merges data into a dict
  def test_beautify(self):
    v = Video('http://www.jeuxvideo.com/gaming-live/0001/00011717/kingdom-hearts-chain-of-memories-gameboy-advance-gba-sora-00000849.htm')
    config = get_video_config()
    info = get_video_info()
    
    expected = build_video().json
    actual = v.beautify(config, info)
    
    self.assertEqual(ordered(actual), ordered(expected))
    
# franck.model.video.Video.load()
class TestVideoLoad(unittest.TestCase):
  
  # check that we don't reload a loaded video and that we get the right object back
  def test_video_no_reload(self):
    with patch('franck.model.video.Video.beautify') as m:
      v = Video('http://www.jeuxvideo.com/foo')
      v.json = 'json was loaded already'
      expected = v
      actual = v.load()
      self.assertEqual(len(m.mock_calls), 0)
      self.assertEqual(id(actual), id(expected))
  
  # check that we load unloaded videos and that we get the right object back
  @patch('franck.model.video.parser.video_config', return_value="video_config")
  @patch('franck.model.video.parser.video_info', return_value="video_info")
  def test_video_load(self, foo, bar):
    with patch('franck.model.video.Video.beautify') as m:
      v = Video('http://www.jeuxvideo.com/foo')
      expected = v
      actual = v.load()
      m.assert_called_once_with('video_config', 'video_info')
      self.assertEqual(id(actual), id(expected))
  
# franck.model.video.Video.__eq__()
class TestVideoEquality(unittest.TestCase):
  # check that a video object is equal to itself
  def test_video_eq_is_same(self):
    v = Video('http://www.jeuxvideo.com/foo')
    self.assertEqual(v, v)
  
  # check that two video objects are equal
  def test_video_eq_is_equal(self):
    v1 = Video('http://www.jeuxvideo.com/foo')
    v2 = Video('http://www.jeuxvideo.com/foo')
    self.assertEqual(v1, v2)
  
  # check that two different video objects are not equal
  def test_video_eq_is_different(self):
    v1 = Video('http://www.jeuxvideo.com/foo')
    v2 = Video('http://www.jeuxvideo.com/bar')
    self.assertFalse(v1 == v2)
  
# franck.model.video.Video.__ne__()
class TestVideoNotEquality(unittest.TestCase):
  # check that a video object is equal to itself
  def test_video_ne_is_same(self):
    v = Video('http://www.jeuxvideo.com/foo')
    self.assertFalse(v != v)
  
  # check that two video objects are equal
  def test_video_ne_is_equal(self):
    v1 = Video('http://www.jeuxvideo.com/foo')
    v2 = Video('http://www.jeuxvideo.com/foo')
    self.assertFalse(v1 != v2)
  
  # check that two different video objects are not equal
  def test_video_ne_is_different(self):
    v1 = Video('http://www.jeuxvideo.com/foo')
    v2 = Video('http://www.jeuxvideo.com/bar')
    self.assertTrue(v1 != v2)
  
if __name__ == '__main__':
  unittest.main()
