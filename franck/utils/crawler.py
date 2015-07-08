#!/usr/bin/python
# -*- coding: utf-8 -*-

# soup stuff goes in here

import sys
import concurrent.futures
from bs4 import BeautifulSoup

import franck.utils.loader as io

BASE_URL = 'http://www.jeuxvideo.com'

def is_video_link(tag):
  return tag.has_attr('href')

def get_soup(url):
  html = io.load_page(url)
  return BeautifulSoup(html, 'html.parser')
  
def get_last_page_index(soup):
  div = soup.find_all("div", class_="bloc-liste-num-page")[0]
  
  try:
    return int(div.find_all("span")[-1].get_text())
  except IndexError:
    return -1
  
# find all the videos on one page
def videos(url):
  try:
    soup = get_soup(url)
    titles = soup.find_all("h2", class_="titre-item")
    links = [h2.find_all("a")[0] for h2 in titles]

    return [BASE_URL + link.get('href') for link in links]
  except:
    return

# returns a list of urls that span the whole section (page 1 to page max)
def index(url):
  soup = get_soup(url)
  page_url = url.split('?')[0]
  
  # get last link, might not be the absolute last (eg 300 out of 303)
  last_page_index = get_last_page_index(soup)
  
  if last_page_index == -1:
    return []
  
  # load last link
  soup = get_soup(page_url + '?p=' + str(last_page_index))
  last_page_index = get_last_page_index(soup)
  
  if last_page_index == -1:
    return []
  
  # return a sorted list of absolute urls for all the pages in the section
  return [page_url + '?p=' + str(i) for i in range(1, int(last_page_index) + 1)]

# returns all the videos found on all pages of one section
# can be run from any page of the section (eg. page 300 of 310)
def crawl(url):
  pages = index(url)
  result = list()
  
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_page = {executor.submit(videos, page): page for page in pages}
    
    for future in concurrent.futures.as_completed(future_to_page):
      print(future)
      result.extend(future.result())
  
  return result

if __name__ == '__main__':
  if len(sys.argv) < 2:
    url = "http://www.jeuxvideo.com/toutes-les-videos/type-7340/?p=296"
  else:
    url = sys.argv[1]
  
  print(crawl(url))
  
