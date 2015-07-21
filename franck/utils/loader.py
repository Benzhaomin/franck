#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import requests

import franck.utils.cache as cache

USER_AGENT = 'Franck/0.4.0'

# returns the content found at a remote url
def _read_page(url):
  try:
    # never ever load something outside of our domain
    if not url.startswith(utils.BASE_URL):
      return ""
      
    #print("[loader] loading " + url)
    headers = {'user-agent': USER_AGENT}
    r = requests.get(url)
    r.raise_for_status()
    return r.text
  except requests.exceptions.HTTPError as e:
    print("[loader] " + str(e) + " error: read_page failed on '"+ url)
    return ""

# returns the content of a remote url, using a local cache
def load_page(url):
  try:
    return cache.read(url)
  except IOError:
    html = _read_page(url)
    cache.write(url, html)
    return html

if __name__ == '__main__':
  if len(sys.argv) < 2:
    url = "http://www.jeuxvideo.com/toutes-les-videos/type-7340/?p=296"
  else:
    url = sys.argv[1]

  #print(len(_read_page(url)))
  #print(len(load_page(url)))
  #print(_read_page(url))
  #print(load_page(url))
