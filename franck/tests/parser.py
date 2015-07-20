#!/usr/bin/env python
# -*- coding: utf-8 -*-

from franck.utils.parser import video_pages
from bs4 import BeautifulSoup

import os
import unittest
from unittest.mock import patch

def get_soup_video_pages(dummy):
  html = open(os.path.join(os.path.dirname(__file__), 'test_video_pages.html')).read()
  return BeautifulSoup(html, 'html.parser')
  
def get_soup_video_pages_404(dummy):
  html = open(os.path.join(os.path.dirname(__file__), 'test_video_pages_404.html')).read()
  return BeautifulSoup(html, 'html.parser')
  
class TestParser(unittest.TestCase):
  
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_video_pages)
  def test_video_pages(self, get_soup_video_pages):   
    expected = ['http://www.jeuxvideo.com/gaming-live/0001/00011717/kingdom-hearts-chain-of-memories-gameboy-advance-gba-sora-00000849.htm', 'http://www.jeuxvideo.com/gaming-live/0001/00011717/kingdom-hearts-chain-of-memories-gameboy-advance-gba-riku-00000848.htm']
    actual = video_pages('http://www.jeuxvideo.com/toutes-les-videos/type-7340/machine-210/genre-2450/')
    self.assertEqual(actual, expected)
    
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_video_pages_404)
  def test_video_pages_404(self, get_soup_video_pages):   
    expected = []
    actual = video_pages('')
    self.assertEqual(actual, expected)

if __name__ == '__main__':
  unittest.main()
