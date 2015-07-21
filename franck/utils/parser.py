#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import re
import hashlib
import concurrent.futures

from bs4 import BeautifulSoup

import franck.utils.loader as io

BASE_URL = 'http://www.jeuxvideo.com'

# return a soup object for the given url, optionaly using a local cache
def _get_soup(url, cache=False):
  html = io.load_page(url)
  return BeautifulSoup(html, 'html.parser')

# returns an absolute url if it's relative
def _get_absolute_url(url):
  if not url.startswith('http'):
    return BASE_URL + url
  return url

# returns the config filename corresponding to a URL
def _get_config_filename(url):
  return hashlib.md5(url.encode()).hexdigest() + ".json"
  
# return the last page number in a section
# TODO: unit test
def _get_last_page_index(soup):
  try:
    div = soup.find_all("div", class_="bloc-liste-num-page")[0]
  
    return int(div.find_all("span")[-1].get_text())
  except IndexError:
    return 0

# returns a list of urls that span the whole section (page 1 to page max)
# TODO: unit test
def index(url):
  soup = _get_soup(url)
  page_url = url.split('?')[0]
  
  # get last link, might not be the absolute last (eg 300 out of 303)
  last_page_index = _get_last_page_index(soup)
  
  if last_page_index == -1:
    return []
  
  # load last link
  soup = _get_soup(page_url + '?p=' + str(last_page_index))
  last_page_index = _get_last_page_index(soup)
  
  if last_page_index == -1:
    return []
  
  # return a sorted list of absolute urls for all the pages in the section
  return [page_url + '?p=' + str(i) for i in range(1, int(last_page_index) + 1)]

# returns the a tag pointing to a video page if any
# TODO: unit test
def _get_video_link(article):
  # try with the standard format (href="/videos/*)
  link = article.find(href=re.compile("^/videos/"))
  
  if not link:
    # custom format links (specific to a section)
    title = article.find("h2", class_="titre-item")

    if title:
      link = title.a
  
  return link
  
# returns a list of url of all the video pages on a page
def video_pages(url):
  soup = _get_soup(url)
  
  # articles often contain videos
  articles = soup.find_all("article")
  
  if not articles:
    return []
  
  # list all links found in articles
  links = [_get_video_link(article) for article in articles]
  
  # remove dead entries (articles without valid link)
  links = filter(None, links)
  
  # return a list of absolute URLs from that list
  return [_get_absolute_url(link.get('href')) for link in links]

# returns the video config file URL from a video page
def video_config_url(url):
  soup = _get_soup(url, cache=True)
  player = soup.find("div", class_="player-jv")
  
  if not player:
    return None
  
  # get the config file url
  return _get_absolute_url(player.get('data-src'))
  
# returns the video json config for a video page
# TODO: unit test
def video_config(url):
  # get the config file url
  config_url = video_config_url(url)
  
  if not config_url:
    return None
  
  config_file = _get_config_filename(url)
  
  # load and cache the config file
  json_config = io.load_page(config_url)

  # turn the json string into a json dict
  return json.loads(json_config)


# returns details about the video on a video page
def video_info(url):
  soup = _get_soup(url, cache=True)
  video = soup.find("div", itemprop="video")
  
  if not video:
    return None
  
  # title: <meta itemprop="name" content="Rocket League : du foot motorisé à l&#039;essai en split-screen !" />
  title = video.find("meta", itemprop="name").get("content")
  
  # thumbnail: <meta itemprop="thumbnail" content="http://image.jeuxvideo.com/images/videos/....jpg" />
  thumbnail = video.find("meta", itemprop="thumbnail").get("content")
  thumbnail = thumbnail.replace('low.jpg', 'high.jpg')
  
  # duration: <meta itemprop="duration" content="PT0H10M37S" />
  duration = video.find("meta", itemprop="duration").get("content")
  
  # <div class="date-comm"> </div>
  #date-comm = video.find("div", itemprop="date-comm")
  
  # datetime: <time datetime="2015-07-09T20:38">09/07/2015 à 20:38</time>
  
  # views: <span>17440 vues</span>
  
  # description (HTML): <div class="corps-video text-enrichi-default">...</div>
  description = video.find("div", class_="corps-video").text
  
  return {
    'title': title,
    'thumbnail': thumbnail,
    'duration': duration,
    'description': description,
  }

    
if __name__ == '__main__':
  if len(sys.argv) < 2:
    url = "http://www.jeuxvideo.com/toutes-les-videos/type-7340/?p=296"
    #url = "http://www.jeuxvideo.com/videos/gaming-live/433637/rocket-league-du-foot-motorise-a-l-essai-en-split-screen.htm"
  else:
    url = sys.argv[1]
  
  #print(index(url))
  #print(video_pages(url))
  print(video_config_url(url))
  print(video_config(url))
  print(video_info(url))
