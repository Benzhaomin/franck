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
  html = io.load_page(url, cache=cache)
  return BeautifulSoup(html, 'html.parser')

# return the last page number in a section
def _get_last_page_index(soup):
  try:
    div = soup.find_all("div", class_="bloc-liste-num-page")[0]
  
    return int(div.find_all("span")[-1].get_text())
  except IndexError:
    return 0
  
# returns a list of urls that span the whole section (page 1 to page max)
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

# returns a list of url of all the video pages on a page
def video_pages(url):
  try:
    soup = _get_soup(url)
    
    # articles often contain videos
    articles = soup.find_all("article")
    
    # list all links found in articles
    links = [article.find("a") for article in articles]
    
    # return a list of absolute URLs from that list
    return [BASE_URL + link.get('href') for link in links]
  except:
    return

# returns the video config file for a video page
def video_config(url):
  try:
    soup = _get_soup(url, cache=True)
    player = soup.find("div", class_="player-jv")
    
    # get the config file url
    config_url = BASE_URL + player.get('data-src')
    config_id = hashlib.md5(url.encode()).hexdigest() + ".json"
    
    # load and cache the config file
    json_config = io.load_page(config_url, filename=config_id)

    # turn the json string into a json dict
    return json.loads(json_config)
  except:
    return

# returns details about the video on a video page
def video_info(url):
  try:
    soup = _get_soup(url, cache=True)
    video = soup.find("div", itemprop="video")
    
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
  except:
    return
    
if __name__ == '__main__':
  if len(sys.argv) < 2:
    url = "http://www.jeuxvideo.com/toutes-les-videos/type-7340/?p=296"
    #url = "http://www.jeuxvideo.com/videos/gaming-live/433637/rocket-league-du-foot-motorise-a-l-essai-en-split-screen.htm"
  else:
    url = sys.argv[1]
  
  #print(index(url))
  print(video_pages(url))
  #print(video_config(url))
  #print(video_info(url))
