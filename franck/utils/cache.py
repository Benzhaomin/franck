#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import string
import datetime
import appdirs
import urllib.parse

import franck.utils.utils as utils

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
    #print("[cache] invalidate?: "+str(expiry)+" "+filename)
    modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    expiry_time = modification_time + expiry
    
    if expiry_time < datetime.datetime.now():
      os.remove(path)
    #  print("[cache] purged: "+filename+str(expiry_time)+'>'+str(datetime.datetime.now()))
    #else:
    #  print("[cache] not too old: "+filename+str(expiry_time)+'<'+str(datetime.datetime.now()))
  
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
  
  #print("[cache] read: "+filename)
  return open(path).read()

def write(uri, content):
  filename = _url_to_filename(uri)
  #print("[cache] write: "+filename)
  path = os.path.join(CACHEDIR, filename)
  
  with open(path, "w+") as cache:
    #print("[cache] will cache: " + str(len(content)))
    cache.write(content)

