#!/usr/bin/env python
# -*- coding: utf-8 -*-

from franck.utils.parser import _get_absolute_url
from franck.utils.parser import _get_config_filename
from franck.utils.parser import video_pages
from franck.utils.parser import video_config_url
from franck.utils.parser import video_config
from franck.utils.parser import video_info
from bs4 import BeautifulSoup

import os
import json
import unittest
from unittest.mock import patch

class TestParserGetAbsoluteUrl(unittest.TestCase):
  def test_get_absolute_url_relative(self):
    expected = 'http://www.jeuxvideo.com/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm'
    actual = _get_absolute_url('/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm')
    self.assertEqual(actual, expected)
    
  def test_get_absolute_url_absolute(self):
    expected = 'http://www.jeuxvideo.com/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm'
    actual = _get_absolute_url('http://www.jeuxvideo.com/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm')
    self.assertEqual(actual, expected)

class TestParserGetConfigFilename(unittest.TestCase):
  def test_get_config_filename(self):
    expected = '34228802351da75aff19169dcdf83c42.json'
    actual = _get_config_filename('http://www.jeuxvideo.com/gaming-live/0001/00011717/kingdom-hearts-chain-of-memories-gameboy-advance-gba-sora-00000849.htm')
    self.assertEqual(actual, expected)
    
# load a remote html file from a local copy and return it as a Soup object
def _get_local_soup(filename):
  with open(os.path.join(os.path.dirname(__file__), 'files', filename)) as htmlfile:
    html = htmlfile.read()
    return BeautifulSoup(html, 'html.parser')
  
def get_soup_homepage(url, cache = None):
  return _get_local_soup('homepage.html')

def get_soup_video_section(url, cache = None):
  return _get_local_soup('video_section.html')
  
def get_soup_video_list(url, cache = None):
  return _get_local_soup('video_list.html')
  
def get_soup_video_page(url, cache = None):
  return _get_local_soup('video_page.html')

def get_soup_404(url, cache = None):
  return _get_local_soup('404.html')
  
def get_soup_no_video(url, cache = None):
  return _get_local_soup('no_video_page.html')
  
class TestParserVideoPages(unittest.TestCase):
  
  # check that we find all video page URLs on the homepage
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_homepage)
  def test_video_pages_homepage(self, get_soup_homepage):   
    expected = ['http://www.jeuxvideo.com/videos/chroniques/435106/le-fond-de-l-affaire-les-secrets-de-league-of-legends.htm', 'http://www.jeuxvideo.com/videos/gaming-live/435104/batgirl-une-affaire-de-famille-qui-tourne-a-la-debandade.htm', 'http://www.jeuxvideo.com/videos/chroniques/435006/merci-dorian-les-adaptations-de-romans.htm', 'http://www.jeuxvideo.com/videos/chroniques/434977/top-10-des-armes-les-plus-emblematiques-et-fun-du-mode-zombies-de-call-of-duty.htm', 'http://www.jeuxvideo.com/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm', 'http://www.jeuxvideo.com/videos/chroniques/434948/au-ceur-de-l-histoire-de-the-witcher-3-episode-4.htm', 'http://www.jeuxvideo.com/videos/433983/call-of-duty-black-ops-une-carte-bonus-pour-le-mode-zombie.htm', 'http://www.jeuxvideo.com/videos/chroniques/434845/l-univers-du-jeu-independant-spectra-le-jeu-musical-8bit.htm', 'http://www.jeuxvideo.com/videos/chroniques/434762/vgm-portal-2.htm', 'http://www.jeuxvideo.com/videos/chroniques/434326/top-10-des-meilleures-scenes-animees-de-minecraft.htm', 'http://www.jeuxvideo.com/videos/chroniques/434220/l-histoire-du-jeu-video-la-saturn.htm', 'http://www.jeuxvideo.com/videos/chroniques/434070/le-fond-de-l-affaire-special-jeux-inde-fez-shovel-knight.htm', 'http://www.jeuxvideo.com/videos/chroniques/433926/le-defi-du-challenge-medhi-et-cdv-s-affrontent-sur-le-theme-des-oiseaux.htm', 'http://www.jeuxvideo.com/videos/chroniques/433900/speed-game-hotline-miami-2-en-moins-de-40-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/433699/l-univers-du-jeu-independant-dolly-de-projet-etudiant-a-plateformer-reussi.htm', 'http://www.jeuxvideo.com/videos/chroniques/433497/pause-process-visual-scripting-la-programmation-pour-tous.htm', 'http://www.jeuxvideo.com/videos/435083/une-petite-dose-de-gameplay-pour-fallout-4.htm', 'http://www.jeuxvideo.com/videos/434357/just-cause-3-6-minutes-de-gameplay-dejante.htm', 'http://www.jeuxvideo.com/videos/435143/rayman-adventures-les-10-premieres-minutes-de-gameplay.htm', 'http://www.jeuxvideo.com/videos/435159/tekken-7-les-costumes-idolmasters-entrent-en-scene.htm', 'http://www.jeuxvideo.com/videos/435057/le-trailer-sanglant-de-tremor-pour-mortal-kombat-x.htm', 'http://www.jeuxvideo.com/videos/435160/un-apercu-de-gameplay-pour-monster-hunter-x.htm', 'http://www.jeuxvideo.com/videos/435110/aurora-dusk-un-age-of-empire-like-independant-francais.htm', 'http://www.jeuxvideo.com/videos/434216/saint-seiya-soldiers-soul-fenrir-vs-dragon-shiryu.htm', 'http://www.jeuxvideo.com/videos/434886/1h-de-gameplay-sur-assassin-s-creed-syndicate.htm']
    actual = video_pages('')
    self.assertEqual(actual, expected)
  
  # check that we find all video page URLs in section pages
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_video_section)
  def test_video_pages_video_section(self, get_soup_video_section):   
    expected = ['http://www.jeuxvideo.com/videos/chroniques/434958/speed-game-live-any-majora-s-mask-fini-en-moins-de-1h35.htm', 'http://www.jeuxvideo.com/videos/chroniques/433900/speed-game-hotline-miami-2-en-moins-de-40-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/432648/speed-game-run-frenetique-sur-ikaruga.htm', 'http://www.jeuxvideo.com/videos/chroniques/431456/speed-game-finir-outlast-en-23-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/430713/speed-game-boucler-twinbee-rba-en-moins-de-26-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/429020/speed-game-boucler-bastion-en-moins-de-15-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/428141/speed-game-donkey-kong-country-tropical-freeze-a-toute-allure.htm', 'http://www.jeuxvideo.com/videos/chroniques/427331/speed-game-une-cyber-run-sur-deus-ex-human-revolution.htm', 'http://www.jeuxvideo.com/videos/chroniques/426604/speed-game-sonic-adventure-2-en-moins-de-30-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/425830/speed-game-s-attaque-au-premier-darksiders.htm', 'http://www.jeuxvideo.com/videos/chroniques/425168/speed-game-okami-hd-fini-en-1h27.htm', 'http://www.jeuxvideo.com/videos/chroniques/424566/speed-game-new-super-mario-bros-wii-fini-en-moins-de-30-minutes.htm', 'http://www.jeuxvideo.com/videos/chroniques/423798/speed-game-une-run-en-live-sur-1001-spikes.htm']
    actual = video_pages('')
    self.assertEqual(actual, expected)
    
  # check that we find all video page URLs in pages with a list of videos
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_video_list)
  def test_video_pages_video_list(self, get_soup_video_list):   
    expected = ['http://www.jeuxvideo.com/gaming-live/0001/00011717/kingdom-hearts-chain-of-memories-gameboy-advance-gba-sora-00000849.htm', 'http://www.jeuxvideo.com/gaming-live/0001/00011717/kingdom-hearts-chain-of-memories-gameboy-advance-gba-riku-00000848.htm']
    actual = video_pages('')
    self.assertEqual(actual, expected)
    
  # check that we get an empty video list on unexisting pages
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_404)
  def test_video_pages_404(self, get_soup_404):   
    expected = []
    actual = video_pages('')
    self.assertEqual(actual, expected)
    
  # check that we get an empty video list on pages without video page URL
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_no_video)
  def test_video_pages_no_video(self, get_soup_no_video):   
    expected = []
    actual = video_pages('')
    self.assertEqual(actual, expected)
  
class TestParserVideoConfigUrl(unittest.TestCase):
  # check that we find the URL of the config file on a video page
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_video_page)
  def test_video_config_url(self, get_soup_video_page):
    expected = 'http://www.jeuxvideo.com/contenu/medias/video.php?q=config&id=60890&autostart=true'
    actual = video_config_url('')
    self.assertEqual(actual, expected)
    
  # check that we get None on unexisting pages
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_404)
  def test_video_config_404(self, get_soup_404):   
    expected = None
    actual = video_config_url('')
    self.assertEqual(actual, expected)
    
  # check that we get None on pages without config
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_no_video)
  def test_video_config_url_no_video(self, get_soup_no_video):   
    expected = None
    actual = video_config_url('')
    self.assertEqual(actual, expected)

# TODO: check that we can load a config file from a video page
class TestParserVideoConfig(unittest.TestCase):
  pass

class TestParserVideoInfo(unittest.TestCase):
  # check that we correctly parse data on a video page
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_video_page)
  def test_video_info(self, get_soup_video_page):
    expected = {'title': 'Kingdom Hearts : Chain of Memories : Sora', 'thumbnail': 'http://image.jeuxvideo.com/images/videos/gaming_live_images/200705/kingdom_hearts_gba-00000849-high.jpg', 'description': "\nRetour sur Chain of Memories, afin de vous remettre les idées au clair concernant cet épisode qui n'est plus vaiment une exclusivité GBA puisque le remake est proposé dans Kingdom Hearts 2 Final Mix+ au Japon. Une bonne occasion de revoir le fonctionnement de ce titre qui se démarque par son système de cartes.\n", 'duration': 'PT0H8M5S'}
    actual = video_info('')
    self.assertEqual(actual, expected)
    
  # check that we get None on unexisting pages
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_404)
  def test_video_config_404(self, get_soup_404):   
    expected = None
    actual = video_info('')
    self.assertEqual(actual, expected)
    
  # check that we get None on pages without config
  @patch('franck.utils.parser._get_soup', side_effect=get_soup_no_video)
  def test_video_config_url_no_video(self, get_soup_no_video):   
    expected = None
    actual = video_info('')
    self.assertEqual(actual, expected)

if __name__ == '__main__':
  unittest.main()
