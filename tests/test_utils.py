#!/usr/bin/env python
# -*- coding: utf-8 -*-

from franck.utils import get_absolute_url
from franck.utils import get_relative_url

import unittest

class TestParserGetAbsoluteUrl(unittest.TestCase):
  def test_get_absolute_url_relative(self):
    expected = 'http://www.jeuxvideo.com/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm'
    actual = get_absolute_url('/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm')
    self.assertEqual(actual, expected)
    
  def test_get_absolute_url_absolute(self):
    expected = 'http://www.jeuxvideo.com/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm'
    actual = get_absolute_url('http://www.jeuxvideo.com/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm')
    self.assertEqual(actual, expected)
    
  def test_get_absolute_url_homepage_slash(self):
    expected = 'http://www.jeuxvideo.com/'
    actual = get_absolute_url('http://www.jeuxvideo.com/')
    self.assertEqual(actual, expected)
    
  def test_get_absolute_url_homepage_noslash(self):
    expected = 'http://www.jeuxvideo.com'
    actual = get_absolute_url('http://www.jeuxvideo.com')
    self.assertEqual(actual, expected)

class TestParserGetRelativeUrl(unittest.TestCase):
  def test_get_relative_url_absolute(self):
    expected = 'videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm'
    actual = get_relative_url('videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm')
    self.assertEqual(actual, expected)
    
  def test_get_relative_url_relative(self):
    expected = 'videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm'
    actual = get_relative_url('videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm')
    self.assertEqual(actual, expected)
    
  def test_get_relative_url_homepage_slash(self):
    expected = 'http://www.jeuxvideo.com/'
    actual = get_relative_url('http://www.jeuxvideo.com/')
    self.assertEqual(actual, expected)
    
  def test_get_relative_url_homepage_noslash(self):
    expected = 'http://www.jeuxvideo.com'
    actual = get_absolute_url('http://www.jeuxvideo.com')
    self.assertEqual(actual, expected)
    
if __name__ == '__main__':
  unittest.main()
