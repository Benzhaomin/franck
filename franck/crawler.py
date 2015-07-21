#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import concurrent.futures

import franck.parser as parser

# returns all the video page url found in a whole section
def crawl(url):
  # get an index of all the pages in the section
  pages = parser.index(url)
  result = []
  
  # parse each page of the section to find video page urls
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_page = {executor.submit(parser.video_pages, page): page for page in pages}
    
    for future in concurrent.futures.as_completed(future_to_page):
      result.extend(future.result())
  
  # list of all the pages containing a video
  return result

if __name__ == '__main__':
  if len(sys.argv) < 2:
    # example: Tous les gaming lives
    url = "http://www.jeuxvideo.com/toutes-les-videos/type-7340/?p=296"
  else:
    url = sys.argv[1]
  
  print(crawl(url))
  
