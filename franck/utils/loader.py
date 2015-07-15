#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import random
import urllib.request, urllib.parse, urllib.error
import unicodedata
import string
import html
  
CACHEDIR = 'cache'


# fake user-agent
class AppURLopener(urllib.request.FancyURLopener):
  version = "Franck Video Downloader - 0.2"

urllib._urlopener = AppURLopener()

def read_page(url):
  try:
    url = urllib.parse.unquote(url)
    url = html.unescape(url)
    #print("loading " + url)
    return urllib.request.urlopen(url).read()
  except urllib.error.HTTPError as e:
    print("failed loading "+ url + " " + str(e.reason) + " " + str(e.code))
    return bin(e.code)
  except IOError:
    print("failed loading "+ url)
    raise

def load_page(url, filename=None, cache=True):
  if cache is True:
    return load_or_cache_page(url, filename)

  return read_page(url).decode()

def load_or_cache_page(url, filename=None):
  try:
    if filename is None:
      filename = url_to_filename(url.split('//')[-1])
    path = os.path.join(os.path.dirname(__file__), CACHEDIR, filename)
    
    # invalidate cache after 1 day for .html
    if filename.endswith(".htm") and os.path.exists(path):
      if os.stat(path).st_mtime < time.time() - 86400:
        os.remove(path)
    
    return open(path).read()
  except IOError:
    #print("time to cache: "+url)
    html = read_page(url)
    #print("will cache: "+html)
    try:
      with open(path, "w+") as cache:
        cache.write(html.decode())

      return open(path).read()
    except AttributeError:
      return "404"

def load_config(config):
  path = os.path.join(os.path.dirname(__file__), CACHEDIR, config)
  
  try:
    return open(path).read()
  except IOError:
    return None

def get_random_config(n=1):
  path = os.path.join(os.path.dirname(__file__), CACHEDIR)
  configs = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith("json")]
  sample = random.sample(configs, min(len(configs),n))
  return [load_config(s) for s in sample]
  
safeChars = "-_. %s%s" % (string.ascii_letters, string.digits)

def url_to_filename(url):
  #url = unicodedata.normalize('NFKD', url).encode('ASCII', 'ignore')
  return ''.join(c for c in url.replace('/', '_') if c in safeChars)
