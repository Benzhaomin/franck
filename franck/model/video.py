#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import json
import time
import hashlib
import xmltodict

import franck.utils.loader as io

BASE_URL = 'http://www.jeuxvideo.com'

VIDEO_BASE_URL = '\/videos\/[a-z]*[\-]?[a-z]*\/'
VIDEO_URL_REGEXP = re.compile('('+VIDEO_BASE_URL + '.*?\.htm)', re.S)

CONFIG_ID_FROM_URL_REGEXP = re.compile(VIDEO_BASE_URL + '\/([\d]*?)\/(.*?).htm', re.S)
CONFIG_ID_FROM_NEWS_URL_REGEXP = re.compile(VIDEO_BASE_URL + '\/([\d]*?)\/(.*?).htm', re.S)
VIDEO_CONFIG_URL_REGEXP = re.compile('class\=\"player\-jv\" [^ ]* data\-src\=\"(\/contenu\/medias\/video\.php\?[^\"]*)\"', re.S)


VIDEO_IFRAME_FROM_SHARING_HTML_REGEXP = re.compile('src="(\/\/www\.jeuxvideo\.com'+VIDEO_BASE_URL+'iframe\/.*?)" ', re.S)
VIDEO_TITLE_FROM_SHARING_HTML_REGEXP = re.compile('\<strong\>(.*?)\<\/strong\>', re.S)

'''
 <a href="/videos/chroniques/413829/tentative-de-run-any-sur-soleil-en-moins-de-50-minutes.htm" title="Speed Game - Tentative de run any% sur Soleil en moins de 50 minutes - MD">
 
http://www.jeuxvideo.com/videos/chroniques/413829/tentative-de-run-any-sur-soleil-en-moins-de-50-minutes.htm
http://www.jeuxvideo.com/videos/gaming-live/414466/monster-hunter-4-ultimate-un-tetsucabra-bien-enervee-2-2.htm

DEAD http://www.jeuxvideo.com/chroniques-video/0005/00054405/chronology-pc-les-coulisses-du-jeu-00123511.htm
http://www.jeuxvideo.com/chroniques-video/00000345/3615-usul-r-d-super-3615-turbo-oniken-pc-00116303.htm

DEAD http://www.jeuxvideo.com/config/ch/0011/6303/00000000_player.xml
http://www.jeuxvideo.com/contenu/medias/video.php?q=config&id=2095387&autostart=true

<div class="embed-responsive-item" >
            <div class="player-jv" id="player-jv-2092299-463" data-src="/contenu/medias/video.php?q=config&amp;id=2092299&amp;autostart=true">Chargement du lecteur vidéo...</div>
        </div>

'''

SECTION_TO_CONFIG = {
    "chroniques": "ch",
    "gaming-live": "gl"
''',
    "videos-editeurs": "ba",
    "reportages-videos-jeux": "re",
    "extraits-videos-jeux": "ex",
    "making-of": "mo"'''
}

class Video:
    
    def __init__(self):
        self.url = None
        self.page = None
        self.config = None
        self.json = None

    def load_page(self):
        # get and cache the html page containing the player config file
        self.page = io.load_page(self.url)
        
    def load_config(self):
        # try to guess the url of the xml file based on the url
        config_url = BASE_URL
        
        # no guessing anymore, could be fixed?
        '''for k,v in SECTION_TO_CONFIG.items():
            if k in self.url:
                config_url += "/".join([v, self.guess_config_url()])
                break'''
        
        # didn't guess a config url
        if config_url == BASE_URL:
            # get the html page to find the config url instead
            if self.page is None:
                self.load_page()
            config_url += VIDEO_CONFIG_URL_REGEXP.findall(self.page)[0]
        
        # load and cache the config file
        json_config = io.load_page(config_url, filename="config_"+self.get_config_id()+".json")
        #print(json_config)
        self.config = json.loads(json_config)
    
    def load(self):
        if self.config is None:
            self.load_config()
        
        return self

    def get_download_url(self):
        return self.get_file_url()
    
    def get_file_url(self):
        return self.config["sources"][0]["file"]
        
    def get_filename(self):
        return io.url_to_filename(self.get_file_url())

    '''
    def guess_config_url(self):
        try:
            (videoid, title) = re.findall(VIDEO_INFOS_FROM_URL_REGEXP, self.url)[0]
            return "/".join([videoid[0:4], videoid[4:8], subpath + "_player.xml"])
        except:
            return ""
    '''
    
    def get_config_id(self):
        try:
            return re.findall(CONFIG_ID_FROM_URL_REGEXP, self.url)[0]
        except:
            # not a single video page, maybe a news
            try:
                return re.findall(CONFIG_ID_FROM_NEWS_URL_REGEXP, self.url)[0]
            except:
                return hashlib.md5(self.url.encode()).hexdigest()
                
    def get_video_id(self):
        try:
            return self.config["related"]["file"].split("=")[-1]
        except:
            # not a single video page, maybe a news
            try:
                return re.findall(CONFIG_ID_FROM_URL_REGEXP, self.url)[0]
            except:
                print (self.config)
                return hashlib.md5(self.url.encode()).hexdigest()
    
    def pretty(self):
        try:
            datemonth = time.mktime(time.strptime(self.json["config"]["file"].split("/")[0], "%Y%m"))
        except:
            datemonth = None
            
        try:
            iframe = 'http://' + re.findall(VIDEO_IFRAME_FROM_SHARING_HTML_REGEXP, self.config["sharing"]["code"])[0]
        except:
            iframe = None
            
        try:
            title = re.findall(VIDEO_TITLE_FROM_SHARING_HTML_REGEXP, self.config["sharing"]["code"])[0]
        except:
            title = ""
        
        return {
            'id': self.get_video_id(),
            'url': self.config["sharing"]["link"],
            'title': title,
            'cover': self.config["image"],
            'sources': { item["label"]: {'file': item["file"], 'size': 0} for item in self.config["sources"]},
            'iframe':  iframe,
        }

import concurrent.futures

def from_url(url):
    try:
        v = Video()
        v.url = url    
        v.load()
        #print("built "+v.url)
        return v
    except Exception as e:
        print("building failed "+v.url+" "+str(e))
        raise e

def from_urls(urls):        
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_video = {executor.submit(from_url, url): url for url in urls}
        
        return filter(None, [future.result() for future in concurrent.futures.as_completed(future_to_video)])

def from_config(config):
    try:
        v = Video()
        v.config = config
        v.load()
        return v
    except:
        return

def from_configs(configs):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_video = {executor.submit(from_config, config): config for config in configs}
        
        return filter(None, [future.result() for future in concurrent.futures.as_completed(future_to_video)])

# get an url:
# - check domain
# - is video page? -> return Videos{thispage}
# - is news page? -> return Videos{thispage}
# - else -> return Videos{crawl thispage}

def get_video_urls(url):
    # bogus URL
    if not url.startswith('http://www.jeuxvideo.com/'):
        return []    

    # is it a video page
    for k,v in SECTION_TO_CONFIG.items():
        if "videos/"+k in url:
            return [url]

    # is it a news page
    if "news/" in url:
        return [url]
    
    # is it a list of video pages then
    page = io.load_page(url, url.split("/")[-1])
    #print("urls found in page: "+str(len(set(re.findall(VIDEO_URL_REGEXP, page)))))
    return set([BASE_URL + u for u in re.findall(VIDEO_URL_REGEXP, page)])

def get_random_config(count):
    try:
        count = int(count)
    except ValueError:
        count = 1
    return [json.loads(c) for c in io.get_random_config(count)]
    
    
def parse(command):
    if command.startswith('http://'):
        return from_urls(get_video_urls(command))
    elif command.startswith("random") or command.startswith("r"):
        return from_configs(get_random_config(command.split(" ")[-1]))
    return []
