#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
import re
from unittest.mock import patch

from bs4 import BeautifulSoup

from franck.parser import video_pages
from franck.parser import video_config_url
from franck.parser import video_config
from franck.parser import video_info
from franck.parser import _get_last_page_index
from franck.parser import index
from franck.parser import _get_video_link

# load a remote html file from a local copy and return it as a Soup object
def get_local_soup(filename):
  with open(os.path.join(os.path.dirname(__file__), 'files', filename)) as htmlfile:
    html = htmlfile.read()
    return BeautifulSoup(html, 'html.parser')

# allow testing recursive index searching
def get_list_soup(url):
  if url.endswith('290'):
    return get_local_soup('video_list_p290.html')
  else:
    return get_local_soup('video_list_p303.html')

def load_video_config(url):
  with open(os.path.join(os.path.dirname(__file__), 'files', 'video_config.json')) as jsondump:
    return jsondump.read()

# recursive ordering (dict/list with nested dict/list)
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

# franck.parser.video_pages()
class TestParserVideoPages(unittest.TestCase):

  # check that we find all video page URLs on the homepage
  @patch('franck.parser._get_soup', return_value=get_local_soup('homepage.html'))
  def test_video_pages_homepage(self, foo):
    expected = ['http://www.jeuxvideo.com/videos/chroniques/435106/le-fond-de-l-affaire-les-secrets-de-league-of-legends.htm', 'http://www.jeuxvideo.com/videos/gaming-live/435104/batgirl-une-affaire-de-famille-qui-tourne-a-la-debandade.htm', 'http://www.jeuxvideo.com/videos/chroniques/435006/merci-dorian-les-adaptations-de-romans.htm', 'http://www.jeuxvideo.com/videos/chroniques/434977/top-10-des-armes-les-plus-emblematiques-et-fun-du-mode-zombies-de-call-of-duty.htm', 'http://www.jeuxvideo.com/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm', 'http://www.jeuxvideo.com/videos/chroniques/434948/au-ceur-de-l-histoire-de-the-witcher-3-episode-4.htm', 'http://www.jeuxvideo.com/videos/433983/call-of-duty-black-ops-une-carte-bonus-pour-le-mode-zombie.htm', 'http://www.jeuxvideo.com/videos/chroniques/434845/l-univers-du-jeu-independant-spectra-le-jeu-musical-8bit.htm', 'http://www.jeuxvideo.com/videos/chroniques/434762/vgm-portal-2.htm', 'http://www.jeuxvideo.com/videos/chroniques/434326/top-10-des-meilleures-scenes-animees-de-minecraft.htm', 'http://www.jeuxvideo.com/videos/chroniques/434220/l-histoire-du-jeu-video-la-saturn.htm', 'http://www.jeuxvideo.com/videos/chroniques/434070/le-fond-de-l-affaire-special-jeux-inde-fez-shovel-knight.htm', 'http://www.jeuxvideo.com/videos/chroniques/433926/le-defi-du-challenge-medhi-et-cdv-s-affrontent-sur-le-theme-des-oiseaux.htm', 'http://www.jeuxvideo.com/videos/chroniques/433900/speed-game-hotline-miami-2-en-moins-de-40-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/433699/l-univers-du-jeu-independant-dolly-de-projet-etudiant-a-plateformer-reussi.htm', 'http://www.jeuxvideo.com/videos/chroniques/433497/pause-process-visual-scripting-la-programmation-pour-tous.htm', 'http://www.jeuxvideo.com/videos/435083/une-petite-dose-de-gameplay-pour-fallout-4.htm', 'http://www.jeuxvideo.com/videos/434357/just-cause-3-6-minutes-de-gameplay-dejante.htm', 'http://www.jeuxvideo.com/videos/435143/rayman-adventures-les-10-premieres-minutes-de-gameplay.htm', 'http://www.jeuxvideo.com/videos/435159/tekken-7-les-costumes-idolmasters-entrent-en-scene.htm', 'http://www.jeuxvideo.com/videos/435057/le-trailer-sanglant-de-tremor-pour-mortal-kombat-x.htm', 'http://www.jeuxvideo.com/videos/435160/un-apercu-de-gameplay-pour-monster-hunter-x.htm', 'http://www.jeuxvideo.com/videos/435110/aurora-dusk-un-age-of-empire-like-independant-francais.htm', 'http://www.jeuxvideo.com/videos/434216/saint-seiya-soldiers-soul-fenrir-vs-dragon-shiryu.htm', 'http://www.jeuxvideo.com/videos/434886/1h-de-gameplay-sur-assassin-s-creed-syndicate.htm']
    actual = video_pages('')
    self.assertEqual(actual, expected)

  # check that we find all video page URLs in section pages
  @patch('franck.parser._get_soup', return_value=get_local_soup('video_section.html'))
  def test_video_pages_video_section(self, foo):
    expected = ['http://www.jeuxvideo.com/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm', 'http://www.jeuxvideo.com/videos/chroniques/433900/speed-game-hotline-miami-2-en-moins-de-40-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/432648/speed-game-run-frenetique-sur-ikaruga.htm', 'http://www.jeuxvideo.com/videos/chroniques/431456/speed-game-finir-outlast-en-23-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/430713/speed-game-boucler-twinbee-rba-en-moins-de-26-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/429020/speed-game-boucler-bastion-en-moins-de-15-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/428141/speed-game-donkey-kong-country-tropical-freeze-a-toute-allure.htm', 'http://www.jeuxvideo.com/videos/chroniques/427331/speed-game-une-cyber-run-sur-deus-ex-human-revolution.htm', 'http://www.jeuxvideo.com/videos/chroniques/426604/speed-game-sonic-adventure-2-en-moins-de-30-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/425830/speed-game-s-attaque-au-premier-darksiders.htm', 'http://www.jeuxvideo.com/videos/chroniques/425168/speed-game-okami-hd-fini-en-1h27.htm', 'http://www.jeuxvideo.com/videos/chroniques/424566/speed-game-new-super-mario-bros-wii-fini-en-moins-de-30-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/423798/speed-game-une-run-en-live-sur-1001-spikes.htm']
    actual = video_pages('')
    self.assertEqual(actual, expected)

  # check that we find all video page URLs in pages with a list of videos
  @patch('franck.parser._get_soup', return_value=get_local_soup('video_list.html'))
  def test_video_pages_video_list(self, foo):
    expected = ['http://www.jeuxvideo.com/gaming-live/0001/00011717/kingdom-hearts-chain-of-memories-gameboy-advance-gba-sora-00000849.htm', 'http://www.jeuxvideo.com/gaming-live/0001/00011717/kingdom-hearts-chain-of-memories-gameboy-advance-gba-riku-00000848.htm']
    actual = video_pages('')
    self.assertEqual(actual, expected)

  # check that we get an empty video list on unexisting pages
  @patch('franck.parser._get_soup', return_value=get_local_soup('404.html'))
  def test_video_pages_404(self, foo):
    expected = []
    actual = video_pages('')
    self.assertEqual(actual, expected)

  # check that we get an empty video list on pages without video page URL
  @patch('franck.parser._get_soup', return_value=get_local_soup('no_video_page.html'))
  def test_video_pages_no_video(self, foo):
    expected = []
    actual = video_pages('')
    self.assertEqual(actual, expected)

# franck.parser.video_config_url()
class TestParserVideoConfigUrl(unittest.TestCase):

  # check that we find the URL of the config file on a video page
  @patch('franck.parser._get_soup', return_value=get_local_soup('video_page.html'))
  def test_video_config_url(self, foo):
    expected = 'http://www.jeuxvideo.com/contenu/medias/video.php?q=config&id=60890&autostart=true'
    actual = video_config_url('')
    self.assertEqual(actual, expected)

  # check that we get None on unexisting pages
  @patch('franck.parser._get_soup', return_value=get_local_soup('404.html'))
  def test_video_config_404(self, foo):
    expected = None
    actual = video_config_url('')
    self.assertEqual(actual, expected)

  # check that we get None on pages without config
  @patch('franck.parser._get_soup', return_value=get_local_soup('no_video_page.html'))
  def test_video_config_url_no_video(self, foo):
    expected = None
    actual = video_config_url('')
    self.assertEqual(actual, expected)

# franck.parser.video_config()
class TestParserVideoConfig(unittest.TestCase):

  # check that we get None on unexisting pages
  @patch('franck.parser.video_config_url', return_value=None)
  def test_video_config_404(self, foo):
    expected = None
    actual = video_config('')
    self.assertEqual(actual, expected)

  # check that we get a proper json dict
  @patch('franck.parser.video_config_url', return_value='http://www.jeuxvideo.com/gaming-live/00000849.htm')
  @patch('franck.parser.loader.load_page', side_effect=load_video_config)
  def test_video_config_has_it(self, foo, bar):
    expected = json.loads(load_video_config(''))
    actual = video_config('')
    self.assertEqual(ordered(actual), ordered(expected))

# franck.parser.video_info()
class TestParserVideoInfo(unittest.TestCase):

  # check that we correctly parse data on a video page
  @patch('franck.parser._get_soup', return_value=get_local_soup('video_page.html'))
  def test_video_info(self, foo):
    expected = {'title': 'Kingdom Hearts : Chain of Memories : Sora', 'thumbnail': 'http://image.jeuxvideo.com/images/videos/gaming_live_images/200705/kingdom_hearts_gba-00000849-high.jpg', 'description': "\nRetour sur Chain of Memories, afin de vous remettre les idées au clair concernant cet épisode qui n'est plus vaiment une exclusivité GBA puisque le remake est proposé dans Kingdom Hearts 2 Final Mix+ au Japon. Une bonne occasion de revoir le fonctionnement de ce titre qui se démarque par son système de cartes.\n", 'duration': 'PT0H8M5S'}
    actual = video_info('')
    self.assertEqual(actual, expected)

  # check that we get None on unexisting pages
  @patch('franck.parser._get_soup', return_value=get_local_soup('404.html'))
  def test_video_info_404(self, foo):
    expected = None
    actual = video_info('')
    self.assertEqual(actual, expected)

# franck.parser._get_last_page_index()
class TestParserGetLastPageIndex(unittest.TestCase):

  # check that we get 0 if there's no index
  def test_get_last_page_noindex(self):
    soup = get_local_soup('404.html')
    expected = 0
    actual = _get_last_page_index(soup)
    self.assertEqual(actual, expected)

  # check that we get the right last page when we are on it already
  def test_get_last_page_is_last_page(self):
    soup = get_local_soup('video_list_p303.html')
    expected = 303
    actual = _get_last_page_index(soup)
    self.assertEqual(actual, expected)

  # check that we get the right last page when we are on some other page
  def test_get_last_page_not_last_page(self):
    soup = get_local_soup('video_list_p290.html')
    expected = 300 # the actual last page isn't shown there
    actual = _get_last_page_index(soup)
    self.assertEqual(actual, expected)

# franck.parser.index()
class TestParserIndex(unittest.TestCase):

  # check that we get an empty list if there's no index
  @patch('franck.parser._get_soup', return_value=get_local_soup('404.html'))
  def test_index_404(self, foo):
    expected = []
    actual = index('url')
    self.assertEqual(actual, expected)
  
  # check that we an empty list if there's no index
  @patch('franck.parser._get_soup', side_effect=get_list_soup)
  def test_index_not_last_page(self, foo):
    expected = ['http://www.jeuxvideo.com/toutes-les-videos/type-7340/?p=' + str(i) for i in range(1, 303+1)]
    actual = index('http://www.jeuxvideo.com/toutes-les-videos/type-7340/?p=290')
    self.assertEqual(actual, expected)
    
def _get_video_link(article):
  # try with the standard format (href="/videos/*)
  link = article.find(href=re.compile("^/videos/"))
  
  if not link:
    # custom format links (specific to a section)
    title = article.find("h2", class_="titre-item")

    if title:
      link = title.a
  
  return link
  
# franck.parser._get_video_link()
class TestParserIndex(unittest.TestCase):
  
  # check that we extract video link from articles whatever their format is
  def test_get_video_link(self):
    soup = get_local_soup('video_thumbnail_examples.html')
    articles = soup.find_all("article")
    
    expected = [
      '/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm',
      '/videos/chroniques/433900/speed-game-hotline-miami-2-en-moins-de-40-minutes.htm',
      '/videos/435083/une-petite-dose-de-gameplay-pour-fallout-4.htm',
      '/videos/435143/rayman-adventures-les-10-premieres-minutes-de-gameplay.htm',
      '/videos/gaming-live/435104/batgirl-une-affaire-de-famille-qui-tourne-a-la-debandade.htm',
      '/gaming-live/0001/00014554/trauma-center-under-the-knife-nintendo-ds-video-3-00000258.htm',
    ]
    actual = [_get_video_link(article).get('href') for article in articles]
    self.assertEqual(actual, expected)
  
  # check that we properly handle articles without links
  def test_get_video_link_no_link(self):
    article = BeautifulSoup("<article/>", 'html.parser')
    
    expected = None
    actual = _get_video_link(article)
    self.assertEqual(actual, expected)

if __name__ == '__main__':
  unittest.main()
