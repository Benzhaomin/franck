#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import string
import datetime
import appdirs
import urllib.parse
import logging

logger = logging.getLogger('franck.logger')

import franck.utils as utils

CACHEDIR = appdirs.user_cache_dir('Franck', 'Wainei')

SHORT_EXPIRY = datetime.timedelta(seconds=300) # 5 minutes
DEFAULT_EXPIRY = datetime.timedelta(seconds=86400) # 1 day

if not os.path.exists(CACHEDIR):
  os.makedirs(CACHEDIR)

def _url_to_filename(url):
  url = utils.get_relative_url(url)
  return urllib.parse.quote(url, safe='')

def _filename_to_url(filename):
  url = urllib.parse.unquote(filename)
  return utils.get_absolute_url(url)

# removes the cached file after some time
def _invalidate(filename, expiry):
  path = os.path.join(CACHEDIR, filename)
  
  if os.path.exists(path):
    logger.debug("[cache] invalidate?: %s, expiring after %s", filename, expiry)
    modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    expiry_time = modification_time + expiry
    
    if expiry_time < datetime.datetime.now():
      os.remove(path)
      logger.debug("[cache] purged: %s because %s > %s", path, expiry_time, datetime.datetime.now())
    else:
      logger.debug("[cache] didn't purge: %s because %s < %s", filename, expiry_time, datetime.datetime.now())
  
# invalidates the cache when necessary
def _refresh(filename):
  # never invalidate config files
  if filename.startswith('contenu%2Fmedias'):
    return
  
  uri = _filename_to_url(filename)
  
  # short cache for lists
  if not uri.endswith('.htm') or utils.get_relative_url(uri).count('/') == 0:
    _invalidate(filename, SHORT_EXPIRY)
    return
  
  # invalidate anything else following the default expiry time
  _invalidate(filename, DEFAULT_EXPIRY)
  
# raises IOError
def read(uri):
  filename = _url_to_filename(uri)
  path = os.path.join(CACHEDIR, filename)
  
  # bypass cache invalidation on new URIs
  if os.path.exists(path):
    _refresh(filename)
  
  logger.debug("[cache] read: %s", filename)
  with open(path) as cached:
    return cached.read()

def write(uri, content):
  filename = _url_to_filename(uri)
  logger.debug("[cache] write: %s", filename)
  path = os.path.join(CACHEDIR, filename)
  
  with open(path, "w+") as cache:
    logger.debug("[cache] will cache: %s characters", len(content))
    cache.write(content)

