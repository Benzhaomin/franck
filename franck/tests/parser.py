#!/usr/bin/env python
# -*- coding: utf-8 -*-

from franck.utils.parser import video_pages

import unittest

class TestParser(unittest.TestCase):
    
    def test_video_pages(self):
      expected = ['http://www.jeuxvideo.com/gaming-live/0001/00011717/kingdom-hearts-chain-of-memories-gameboy-advance-gba-sora-00000849.htm', 'http://www.jeuxvideo.com/gaming-live/0001/00011717/kingdom-hearts-chain-of-memories-gameboy-advance-gba-riku-00000848.htm']
      actual = video_pages('http://www.jeuxvideo.com/toutes-les-videos/type-7340/machine-210/genre-2450/')
      self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()
