#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import datetime
from unittest.mock import patch, mock_open

from franck.io.cache import SHORT_EXPIRY
from franck.io.cache import DEFAULT_EXPIRY
from franck.io.cache import CACHEDIR
from franck.io.cache import _url_to_filename
from franck.io.cache import _filename_to_url
from franck.io.cache import _get_cache_policy
from franck.io.cache import _is_expired
from franck.io.cache import _expire
from franck.io.cache import read
from franck.io.cache import write

# franck.io.cache._url_to_filename()
class TestCacheUrlToFilename(unittest.TestCase):
  
  # check that we get a proper filename for a normal url
  def test_url_to_filename_normal_url(self):
    expected = 'toutes-les-videos%2Fmachine-10%2Fgenre-2240%2F'
    actual = _url_to_filename('http://www.jeuxvideo.com/toutes-les-videos/machine-10/genre-2240/')
    self.assertEqual(actual, expected)
    
  # check that we get a proper filename for the homepage
  def test_url_to_filename_homepage(self):
    expected = 'http%3A%2F%2Fwww.jeuxvideo.com%2F'
    actual = _url_to_filename('http://www.jeuxvideo.com/')
    self.assertEqual(actual, expected)

# franck.io.cache._filename_to_url()
class TestCacheFilenameToUrl(unittest.TestCase):
  
  # check that we get a proper filename for a normal url
  def test_filename_to_url_normal_url(self):
    expected = 'http://www.jeuxvideo.com/toutes-les-videos/machine-10/genre-2240/'
    actual = _filename_to_url('toutes-les-videos%2Fmachine-10%2Fgenre-2240%2F')
    self.assertEqual(actual, expected)
    
  # check that we get a proper filename for the homepage
  def test_filename_to_url_homepage(self):
    expected = 'http://www.jeuxvideo.com/'
    actual = _filename_to_url('http%3A%2F%2Fwww.jeuxvideo.com%2F')
    self.assertEqual(actual, expected)
  
# franck.io.cache._get_cache_policy()
class TestCacheGetCachePolicy(unittest.TestCase):
  
  # check that basic pages use the default expiry time
  def test_get_cache_policy_video_page(self):
    expected = DEFAULT_EXPIRY
    actual = _get_cache_policy('videos%2Fchroniques%2F427331%2Fspeed-game-une-cyber-run-sur-deus-ex-human-revolution.htm')
    self.assertEqual(actual, expected)
  
  # check that generated lists use the short expiry time
  def test_get_cache_policy_video_list(self):
    expected = SHORT_EXPIRY
    actual = _get_cache_policy('toutes-les-videos%2Ftype-7340%2Fmachine-110%2F%3Fp%3D2')
    self.assertEqual(actual, expected)
  
  # check that the homepage uses the short expiry time
  def test_get_cache_policy_homepage(self):
    expected = SHORT_EXPIRY
    actual = _get_cache_policy('http%3A%2F%2Fwww.jeuxvideo.com%2F')
    self.assertEqual(actual, expected)
  
  # check that config files don't expire
  def test_get_cache_policy_config_file(self):
    expected = None
    actual = _get_cache_policy('contenu%2Fmedias%2Fvideo.php%3Fq%3Dconfig%26id%3D2151308%26autostart%3Dtrue')
    self.assertEqual(actual, expected)

# franck.io.cache._is_expired()
class TestCacheIsExpired(unittest.TestCase):
  
  # check that expired file expire
  @patch('franck.io.cache.os.path.getmtime', return_value=(datetime.datetime.now()-DEFAULT_EXPIRY).replace(tzinfo=datetime.timezone.utc).timestamp())
  def test_is_expired_expired(self, foo):
    expected = True
    actual = _is_expired('', SHORT_EXPIRY)
    self.assertEqual(actual, expected)
  
  # check that valid files are still valid
  @patch('franck.io.cache.os.path.getmtime', return_value=(datetime.datetime.now()-SHORT_EXPIRY).replace(tzinfo=datetime.timezone.utc).timestamp())
  def test_is_expired_valid(self, foo):
    expected = False
    actual = _is_expired('', DEFAULT_EXPIRY)
    self.assertEqual(actual, expected)
  
# franck.io.cache._expire()
class TestCacheExpire(unittest.TestCase):
  
  # check that we remove expired files
  @patch('franck.io.cache._is_expired', return_value=True)  
  def test_expire_expired(self, foo):
    filename = 'somefile'
    path = os.path.join(CACHEDIR, filename)
    
    # make sure os.remove was called on the cached file
    with patch('franck.io.cache.os.remove') as m:
      _expire(filename)
      m.assert_called_once_with(path)
  
  # check that we don't purge valid files
  @patch('franck.io.cache._is_expired', return_value=False)  
  def test_expire_not_expired(self, foo):
    filename = 'somefile'
    
    # make sure os.remove was not called
    with patch('franck.io.cache.os.remove') as m:
      _expire(filename)
      self.assertEqual(len(m.mock_calls), 0)
  
# franck.io.cache.read()
class TestCacheRead(unittest.TestCase):
  
  # check that we properly read the content of a cached file
  def test_read_file_exists(self):
    uri = 'http://www.jeuxvideo.com/'
    filename = _url_to_filename(uri)
    path = os.path.join(CACHEDIR, filename)
    expected = '{data}'
    
    # mock open with some data and check it was called
    with patch('franck.io.cache.open', mock_open(read_data=expected), create=True) as m:
      actual = read(uri)
      m.assert_called_once_with(path)
      self.assertEqual(actual, expected)
  
  # check that we get a FileNotFoundError when trying to read a unexisting file
  def test_read_ioerror(self):
    self.assertRaises(FileNotFoundError, read, "unexisting file")
  
# franck.io.cache.write()
class TestCacheWrite(unittest.TestCase):
  
  # check that we properly write content to a cached file
  def test_write_file(self):
    uri = 'http://www.jeuxvideo.com/'
    filename = _url_to_filename(uri)
    path = os.path.join(CACHEDIR, filename)
    expected = '{data}'
    
    # mock open with some data and check it was called
    with patch('franck.io.cache.open', mock_open(read_data=expected), create=True) as m:
      write(uri, expected)
      m.assert_called_once_with(path, 'w+')
      handle = m()
      handle.write.assert_called_once_with(expected)
  
if __name__ == '__main__':
  unittest.main()
