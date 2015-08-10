#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from unittest.mock import patch

from franck.api import videos
from franck.api import video

from franck.model.video import Video

def build_video(url):
  return Video(url)

# franck.api.videos()
class TestApiVideos(unittest.TestCase):

  # check that we request parsing and return a list of results
  @patch('franck.api.parser.video_pages', return_value=['http://www.jeuxvideo.com/foo', 'http://www.jeuxvideo.com/bar', 'http://www.jeuxvideo.com/baz'])
  @patch('franck.api.video', side_effect=build_video)
  def test_api_videos(self, foo, bar):
    expected = [Video('http://www.jeuxvideo.com/foo'), Video('http://www.jeuxvideo.com/bar'), Video('http://www.jeuxvideo.com/baz')]
    actual = videos('http://www.jeuxvideo.com/list')
    self.assertEqual(actual, expected)

  # check that we return an empty list when there are no results
  @patch('franck.api.parser.video_pages', return_value=[])
  @patch('franck.api.video', side_effect=build_video)
  def test_api_videos_no_result(self, foo, bar):
    expected = []
    actual = videos('http://www.jeuxvideo.com/novideo')
    self.assertEqual(actual, expected)

# franck.api.video()
class TestApiVideo(unittest.TestCase):

  # check that we build a Video object and load it
  def test_api_video(self):
    with patch('franck.model.video.Video.load') as m:
      expected = Video('http://www.jeuxvideo.com/foo')
      actual = video('http://www.jeuxvideo.com/foo')
      self.assertEqual(actual, expected)
      m.assert_called_once_with()

if __name__ == '__main__':
  unittest.main()
