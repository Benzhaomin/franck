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

# franck.model.video.Video.get_best_quality()
class TestVideoGetBestQuality(unittest.TestCase):

  # check that we handle unloaded videos
  def test_get_best_quality_unloaded(self):
    v = Video('http://www.jeuxvideo.com/foo')
    expected = None
    actual = v.get_best_quality()
    self.assertEqual(actual, expected)

  # check that we get the best quality available
  def test_get_best_quality_has_400p(self):
    v = build_video()
    expected = '400p'
    actual =  v.get_best_quality()
    self.assertEqual(actual, expected)

  # check that we get nothing if there's no source at all
  def test_get_best_quality_no_source(self):
    v = build_video()
    v.json['sources'] = {}
    expected = None
    actual = v.get_best_quality()
    self.assertEqual(actual, expected)

# franck.model.video.Video.get_source()
class TestVideoGetSource(unittest.TestCase):

  # check that we handle unloaded videos
  def test_get_source_unloaded(self):
    v = Video('http://www.jeuxvideo.com/foo')
    expected = None
    actual = v.get_source()
    self.assertEqual(actual, expected)

  # check that we handle empty quality requests
  def test_get_source_none_quality(self):
    v = build_video()
    expected = 'http://videohd.jeuxvideo.com/200705/kingdom_hearts_gba-00000849-high.mp4'
    actual = v.get_source(quality=None)['file']
    self.assertEqual(actual, expected)

  # check that we handle invalid quality requests
  def test_get_source_foo_quality(self):
    v = build_video()
    expected = 'http://videohd.jeuxvideo.com/200705/kingdom_hearts_gba-00000849-high.mp4'
    actual = v.get_source('foo')['file']
    self.assertEqual(actual, expected)

  # check that the quality is auto-selected if missing, want default (1080p) has 400p max
  def test_get_source_default_quality_auto_select(self):
    v = build_video()
    expected = 'http://videohd.jeuxvideo.com/200705/kingdom_hearts_gba-00000849-high.mp4'
    actual = v.get_source()['file']
    self.assertEqual(actual, expected)

  # check that the quality is correct, want 272p, has 400p too, ignored
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


# franck.model.video.Video.loaded()
class TestVideoLoaded(unittest.TestCase):

  # check that a new video is unloaded
  def test_video_loaded_load(self):
    v = Video('http://www.jeuxvideo.com/foo')
    expected = False
    actual = v.loaded()
    self.assertEqual(actual, expected)

  # check that a loaded video is loaded
  def test_video_loaded_load(self):
    v = Video('http://www.jeuxvideo.com/foo')
    v.json = 'json was loaded already'
    expected = True
    actual = v.loaded()
    self.assertEqual(actual, expected)

# franck.model.video.Video.valid()
class TestVideoValid(unittest.TestCase):

  # check that a new video is invalid
  def test_video_valid_unloaded(self):
    v = Video('http://www.jeuxvideo.com/foo')
    expected = False
    actual = v.valid()
    self.assertEqual(actual, expected)

  # check that a valid video is valid
  def test_video_valid_loaded_valid(self):
    v = Video('http://www.jeuxvideo.com/foo')
    v.json = 'json was loaded already'
    expected = True
    actual = v.valid()
    self.assertEqual(actual, expected)

  # check that an invalid video is valid
  def test_video_valid_loaded_invalid(self):
    v = Video('http://www.jeuxvideo.com/foo')
    v.json = {}
    expected = False
    actual = v.valid()
    self.assertEqual(actual, expected)

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
