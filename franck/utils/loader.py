#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import unicodedata
import string
import html
import requests
import appdirs

CACHEDIR = appdirs.user_cache_dir('Franck', 'Wainei')

if not os.path.exists(CACHEDIR):
  os.makedirs(CACHEDIR)

# TODO: check that we never load any page outside of jeuxvideo.com/
def read_page(url):
  try:
    print("loading " + url)
    headers = {'user-agent': 'Franck/0.4.0'}
    r = requests.get(url)
    r.raise_for_status()
    return r.text
  except requests.exceptions.HTTPError as e:
    print(str(e) + " error: read_page failed on '"+ url)
    return ""

def load_page(url, filename=None, cache=True):
  if cache is True:
    return load_or_cache_page(url, filename)

  return read_page(url)

def load_or_cache_page(url, filename=None):
  try:
    if filename is None:
      filename = url_to_filename(url.split('//')[-1])
    path = os.path.join(CACHEDIR, filename)
    
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
  path = os.path.join(CACHEDIR, config)
  
  try:
    return open(path).read()
  except IOError:
    return None

def get_random_config(n=1):
  path = CACHEDIR
  configs = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith("json")]
  sample = random.sample(configs, min(len(configs),n))
  return [load_config(s) for s in sample]
  
safeChars = "-_. %s%s" % (string.ascii_letters, string.digits)

def url_to_filename(url):
  #url = unicodedata.normalize('NFKD', url).encode('ASCII', 'ignore')
  return ''.join(c for c in url.replace('/', '_') if c in safeChars)

if __name__ == '__main__':
  if len(sys.argv) < 2:
    url = "http://www.jeuxvideo.com/toutes-les-videos/type-7340/?p=296"
  else:
    url = sys.argv[1]

  print(len(load_page(url, cache=False)))
  #print(len(load_page(url, cache=True)))
  #print(load_page(url, cache=False))
  #print(load_page(url, cache=True))
