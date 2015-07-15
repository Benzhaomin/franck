#!/usr/bin/python
# -*- coding: utf-8 -*-

import concurrent.futures

import franck.utils.parser as parser

# returns all the video url found on all pages of one section
# can be run from any page of the section (eg. page 300 of 310)
def crawl(url):
  # get an index of all the pages in the section
  pages = parser.index(url)
  result = list()
  
  # parse each page of the section to find video page urls
  with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_page = {executor.submit(parser.video_pages, page): page for page in pages}
    
    for future in concurrent.futures.as_completed(future_to_page):
      result.extend(future.result())
  
  # list of all the pages containing a video
  return result

if __name__ == '__main__':
  if len(sys.argv) < 2:
    url = "http://www.jeuxvideo.com/toutes-les-videos/type-7340/?p=296"
  else:
    url = sys.argv[1]
  
  print(crawl(url))
  
