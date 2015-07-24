#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from unittest.mock import patch
import requests

from franck.io.loader import _read_page
from franck.io.loader import load_page

def get_valid_response(url):
  response = requests.Response()
  response._content = b'<html/>'
  response.status_code = 200
  return response

def get_404_response(url):
  response = requests.Response()
  response.status_code = 404
  return response

def cache_read_failed(url):
  raise FileNotFoundError()

# franck.io.loader._read_page()
class TestLoaderReadPage(unittest.TestCase):

  # check that we properly get a page's content
  @patch('franck.io.loader.requests.get', side_effect=get_valid_response)
  def test_read_page_has_content(self, foo):
    expected = '<html/>'
    actual = _read_page('http://www.jeuxvideo.com/')
    self.assertEqual(actual, expected)
   
  # check that urls outside of the main domain are rejected
  def test_read_page_outside_url(self):
    expected = ""
    actual = _read_page('http://www.nottherightdomain.com/')
    self.assertEqual(actual, expected)
  
  # check that 404 errors are handled
  @patch('franck.io.loader.requests.get', side_effect=get_404_response)
  def test_read_page_404(self, foo):
    expected = ""
    actual = _read_page('http://www.jeuxvideo.com/404')
    self.assertEqual(actual, expected)

# franck.io.loader.load_page()
class TestLoaderLoadPage(unittest.TestCase):
    
  # check that pages are read from cache
  @patch('franck.io.loader.cache.read', return_value='<html/>')
  def test_load_page_from_cache(self, foo):
    expected = "<html/>"
    actual = load_page('http://www.jeuxvideo.com/')
    self.assertEqual(actual, expected)
    
  # check that uncached pages are loaded and written to cache
  @patch('franck.io.loader.cache.read', side_effect=cache_read_failed)
  @patch('franck.io.loader._read_page', return_value='<html/>')
  def test_load_page_write_cache(self, foo, bar):
    expected = "<html/>"
    # make sure cache.write was called to the cache the page
    with patch('franck.io.loader.cache.write') as m:
      actual = load_page('http://www.jeuxvideo.com/')
      m.assert_called_once_with('http://www.jeuxvideo.com/', "<html/>")
      self.assertEqual(actual, expected)  
  
  
if __name__ == '__main__':
  unittest.main()
