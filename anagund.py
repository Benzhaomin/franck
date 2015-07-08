#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

import franck.utils.crawler as crawler

'''
  Prints the url of all pages in a given section, eg:
  
  $ anagund.py "http://www.jeuxvideo.com/toutes-les-videos/type-7340/machine-20/genre-2570/"
   
  http://www.jeuxvideo.com/videos/gaming-live/422556/mortal-kombat-x-que-faire-apres-la-kampagne.htm
  http://www.jeuxvideo.com/videos/gaming-live/418299/dragon-ball-xenoverse-petite-visite-de-tokitoki.htm
  http://www.jeuxvideo.com/videos/gaming-live/417880/last-round-l-ultime-version-de-dead-or-alive-5.htm
  http://www.jeuxvideo.com/gaming-live/0005/00052812/wwe-2k15-xbox-one-1-2-john-cena-raie-mysterio-de-la-carte-00124557.htm
  http://www.jeuxvideo.com/gaming-live/0005/00052812/wwe-2k15-xbox-one-2-2-un-contenu-ampute-00124559.htm
  http://www.jeuxvideo.com/gaming-live/0004/00048779/ea-sports-ufc-xbox-one-des-mecs-en-slip-de-gros-muscles-et-beaucoup-de-violence-00121357.htm
'''
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("what page?")
    sys.exit(1)

  for url in crawler.crawl(sys.argv[1]):
    print(url)
