#!/usr/bin/python
# -*- coding: utf-8 -*-

BASE_URL = 'http://www.jeuxvideo.com/'

# returns an absolute url if it's relative
def get_absolute_url(url):
  if not url.startswith(BASE_URL.rstrip('/')):
    return BASE_URL + url.lstrip('/')
  return url
  
def get_relative_url(url):
  # careful about a relative url to the homepage
  if url.startswith(BASE_URL) and len(BASE_URL) < len(url):
    return url[len(BASE_URL):]
  return url
