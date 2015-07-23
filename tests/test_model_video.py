#!/usr/bin/env python
# -*- coding: utf-8 -*-

from franck.model.video import Video

import unittest

def build_video():
  v = Video('')
  v.json = {
    "title": "Rocket League : du foot motoris\u00e9 \u00e0 l'essai en split-screen !",
    "cover": "http://image.jeuxvideo.com/images/videos/gaming_live_images/r/o/rocket-league-pc-121917-1436453790-high.jpg",
    "id": "2150407",
    "url": "http://www.jeuxvideo.com/videos/gaming-live/433637/rocket-league-du-foot-motorise-a-l-essai-en-split-screen.htm",
    "description": "\nNous connaissance sur le jeu.\n",
    "timeline": "http://image.jeuxvideo.com/images/videos/gaming_live_images/r/o/rocket-league-pc-121917-1436453790-0000.jpg",
    "sources": {
      "720p": {"size": 0, "file": "http://video720.jeuxvideo.com/gaming-live/r/o/rocket-league-pc-121917-1436453790-720p.mp4"},
      "272p": {"size": 0, "file": "http://video.jeuxvideo.com/gaming-live/r/o/rocket-league-pc-121917-1436453790-low.mp4"},
      "400p": {"size": 0, "file": "http://videohd.jeuxvideo.com/gaming-live/r/o/rocket-league-pc-121917-1436453790-high.mp4"},
      "1080p": {"size": 0, "file": "http://video1080.jeuxvideo.com/gaming-live/r/o/rocket-league-pc-121917-1436453790-1080p.mp4"}
    },
    "iframe": "http://www.jeuxvideo.com/videos/iframe/2150407"
  }
  return v
  
  
class TestVideoGetSource(unittest.TestCase):
  # want default (1080p) has it
  def test_get_source_default_quality_has_it(self):
    v = build_video()
    expected = 'http://video1080.jeuxvideo.com/gaming-live/r/o/rocket-league-pc-121917-1436453790-1080p.mp4'
    actual = v.get_source()['file']
    self.assertEqual(actual, expected)
    
  # want default (1080p) has 720p max
  def test_get_source_default_quality_auto_select(self):
    v = build_video()
    del v.json["sources"]["1080p"]
    expected = 'http://video720.jeuxvideo.com/gaming-live/r/o/rocket-league-pc-121917-1436453790-720p.mp4'
    actual = v.get_source()['file']
    self.assertEqual(actual, expected)
    
  # want default (720p) has it
  def test_get_source_720p_quality_has_it(self):
    v = build_video()
    expected = 'http://video720.jeuxvideo.com/gaming-live/r/o/rocket-league-pc-121917-1436453790-720p.mp4'
    actual = v.get_source('720p')['file']
    self.assertEqual(actual, expected)

    
if __name__ == '__main__':
  unittest.main()
