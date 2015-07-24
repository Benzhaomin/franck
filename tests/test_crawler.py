#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

from franck.crawler import crawl

def get_video_pages(url):
  if url.endswith('?p=1'):
    return ['http://www.jeuxvideo.com/gaming-live/0004/00046186/might-magic-heroes-online-web-des-heros-dans-votre-navigateur-00123587.htm', 'http://www.jeuxvideo.com/gaming-live/0005/00052128/star-made-pc-un-minecraft-galactique-00120075.htm', 'http://www.jeuxvideo.com/gaming-live/0005/00051725/contract-wars-web-les-guerres-de-contrat-00120071.htm', 'http://www.jeuxvideo.com/gaming-live/0005/00051659/begone-web-un-petit-fps-gratuit-et-bien-nerveux-00119370.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-visite-de-jvcraft-00115282.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00045032/game-of-thrones-ascent-web-un-free-to-play-a-westeros-00112172.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00048243/le-hobbit-armees-du-troisieme-age-web-un-jeu-web-comme-il-en-existe-des-centaines-00111883.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00046482/mush-web-la-chasse-aux-champignons-tueurs-00111405.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00046224/kartuga-web-preview-du-sang-dans-l-ocean-00110962.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00046185/anno-online-web-preview-sur-la-beta-fermee-00110955.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00047765/crystal-saga-web-un-mmo-free-to-play-plutot-sympathique-00110510.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00047760/ski-challenge-2013-web-peu-de-nouveautes-mais-un-concept-toujours-aussi-fun-00110320.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00044779/alt-minds-web-dans-la-peau-d-un-veritable-enqueteur-00108292.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00045665/ninja-tooken-web-la-fine-fleur-des-jeux-web-00005009.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00043175/brick-force-web-fps-en-kit-00004980.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00043122/command-conquer-tiberium-alliances-web-un-jeu-web-classique-mais-efficace-00004883.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00043251/blackwell-web-un-gaming-live-a-pas-de-loup-00004564.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00043289/8-realms-web-un-settlers-like-sympathique-00004593.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-un-nouveau-commencement-00004437.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00039210/drakensang-online-web-1-2-un-vrai-mmo-hack-n-slash-00004239.htm'];
  elif url.endswith('?p=2'):
    return ['http://www.jeuxvideo.com/gaming-live/0003/00039210/drakensang-online-web-2-2-pas-de-chocolat-pas-de-mana-00004240.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-ou-l-on-fait-monter-la-temperature-00003907.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-retour-a-jiveville-00003874.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-1-4-rendez-vous-en-terre-inconnue-00003835.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-2-4-l-ami-creeper-du-petit-dejeuner-00003836.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-3-4-horizons-lointains-00003837.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-4-4-petits-delires-entre-amis-00003838.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00037188/star-wars-clone-wars-adventures-web---00003683.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00034658/wakfu-les-gardiens-web-de-la-serie-au-jeu-web-00002931.htm', 'http://www.jeuxvideo.com/gaming-live/0002/00029373/auditorium-web-un-puzzle-game-pour-melomanes-00002277.htm', 'http://www.jeuxvideo.com/gaming-live/0002/00021197/quake-live-web-mode-deathmatch-00002211.htm', 'http://www.jeuxvideo.com/gaming-live/0002/00021197/quake-live-web---00002212.htm'];
  return ''

# recursive ordering (dict/list with nested dict/list)
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

# franck.parser.video_pages()
class TestCrawlerCrawl(unittest.TestCase):

  # check that we find all video page URLs in a 2 pages section
  @patch('franck.crawler.parser.index', return_value=['http://www.jeuxvideo.com/toutes-les-videos/type-7340/machine-110/?p=1', 'http://www.jeuxvideo.com/toutes-les-videos/type-7340/machine-110/?p=2'])
  @patch('franck.crawler.parser.video_pages', side_effect=get_video_pages)
  def test_crawl_2_pages(self, foo, bar):
    expected = ['http://www.jeuxvideo.com/gaming-live/0003/00039210/drakensang-online-web-2-2-pas-de-chocolat-pas-de-mana-00004240.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-ou-l-on-fait-monter-la-temperature-00003907.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-retour-a-jiveville-00003874.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-1-4-rendez-vous-en-terre-inconnue-00003835.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-2-4-l-ami-creeper-du-petit-dejeuner-00003836.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-3-4-horizons-lointains-00003837.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-4-4-petits-delires-entre-amis-00003838.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00037188/star-wars-clone-wars-adventures-web---00003683.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00034658/wakfu-les-gardiens-web-de-la-serie-au-jeu-web-00002931.htm', 'http://www.jeuxvideo.com/gaming-live/0002/00029373/auditorium-web-un-puzzle-game-pour-melomanes-00002277.htm', 'http://www.jeuxvideo.com/gaming-live/0002/00021197/quake-live-web-mode-deathmatch-00002211.htm', 'http://www.jeuxvideo.com/gaming-live/0002/00021197/quake-live-web---00002212.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00046186/might-magic-heroes-online-web-des-heros-dans-votre-navigateur-00123587.htm', 'http://www.jeuxvideo.com/gaming-live/0005/00052128/star-made-pc-un-minecraft-galactique-00120075.htm', 'http://www.jeuxvideo.com/gaming-live/0005/00051725/contract-wars-web-les-guerres-de-contrat-00120071.htm', 'http://www.jeuxvideo.com/gaming-live/0005/00051659/begone-web-un-petit-fps-gratuit-et-bien-nerveux-00119370.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-visite-de-jvcraft-00115282.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00045032/game-of-thrones-ascent-web-un-free-to-play-a-westeros-00112172.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00048243/le-hobbit-armees-du-troisieme-age-web-un-jeu-web-comme-il-en-existe-des-centaines-00111883.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00046482/mush-web-la-chasse-aux-champignons-tueurs-00111405.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00046224/kartuga-web-preview-du-sang-dans-l-ocean-00110962.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00046185/anno-online-web-preview-sur-la-beta-fermee-00110955.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00047765/crystal-saga-web-un-mmo-free-to-play-plutot-sympathique-00110510.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00047760/ski-challenge-2013-web-peu-de-nouveautes-mais-un-concept-toujours-aussi-fun-00110320.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00044779/alt-minds-web-dans-la-peau-d-un-veritable-enqueteur-00108292.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00045665/ninja-tooken-web-la-fine-fleur-des-jeux-web-00005009.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00043175/brick-force-web-fps-en-kit-00004980.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00043122/command-conquer-tiberium-alliances-web-un-jeu-web-classique-mais-efficace-00004883.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00043251/blackwell-web-un-gaming-live-a-pas-de-loup-00004564.htm', 'http://www.jeuxvideo.com/gaming-live/0004/00043289/8-realms-web-un-settlers-like-sympathique-00004593.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00038024/minecraft-web-un-nouveau-commencement-00004437.htm', 'http://www.jeuxvideo.com/gaming-live/0003/00039210/drakensang-online-web-1-2-un-vrai-mmo-hack-n-slash-00004239.htm']
    actual = crawl('')
    self.assertEqual(ordered(actual), ordered(expected))
    
  # check that we get handle empty pages
  @patch('franck.crawler.parser.index', return_value=[])
  @patch('franck.crawler.parser.video_pages', return_value=[])
  def test_crawl_404(self, foo, bar):
    expected = []
    actual = crawl('')
    self.assertEqual(ordered(actual), ordered(expected))


if __name__ == '__main__':
  unittest.main()
