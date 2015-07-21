#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import requests

import franck.utils.cache as cache

# TODO: check that we never load any page outside of jeuxvideo.com/
def _read_page(url):
  try:
    print("[loader] loading " + url)
    headers = {'user-agent': 'Franck/0.4.0'}
    r = requests.get(url)
    r.raise_for_status()
    return r.text
  except requests.exceptions.HTTPError as e:
    print("[loader] " + str(e) + " error: read_page failed on '"+ url)
    return ""

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

  #print(len(load_page(url, cache=False)))
  print(len(load_page(url, cache=True)))
  #print(load_page(url, cache=False))
  #print(load_page(url, cache=True))
