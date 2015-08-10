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

# returns a datetime equal to the max lifetime of a cached file depending on its kind
def _get_cache_policy(filename):
  # never invalidate config files
  if filename.startswith('contenu%2Fmedias'):
    return None

  uri = _filename_to_url(filename)

  # short cache for lists
  if not uri.endswith('.htm') or utils.get_relative_url(uri).count('/') == 0:
    return SHORT_EXPIRY

  # anything else follows the default expiry time
  return DEFAULT_EXPIRY

# removes cached files if expired
def _is_expired(filename, expiry):
  if expiry is None:
    return False

  path = os.path.join(CACHEDIR, filename)
  modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(path))
  expiry_time = modification_time + expiry

  return expiry_time < datetime.datetime.now()

# check the current cache in case this file is there but expired
def _expire(filename):
  # find out when the file should expire and check if it has
  expiry = _get_cache_policy(filename)
  expired = _is_expired(filename, expiry)

  # remove expired files from disk
  if expired:
    os.remove(os.path.join(CACHEDIR, filename))
    logger.debug("[cache] cached file purged: %s", filename)
  else:
    logger.debug("[cache] cached file still valid: %s", filename)

# returns the contents of the cached file for that uri, raises FileNotFoundError
def read(uri):
  filename = _url_to_filename(uri)
  path = os.path.join(CACHEDIR, filename)
  logger.debug("[cache] read: %s", filename)

  # remove old cache file
  if os.path.exists(path):
    _expire(filename)

  # read the file from disk
  with open(path) as cached:
    return cached.read()

# cache content found at that uri to a file
def write(uri, content):
  filename = _url_to_filename(uri)
  path = os.path.join(CACHEDIR, filename)
  logger.debug("[cache] write: %s %s characters", filename, len(content))

  # write the content to disk
  with open(path, "w+") as cache:
    cache.write(content)

