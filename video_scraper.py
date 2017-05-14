import scrapy
from scrapy.crawler import CrawlerProcess
import json
import os
import datetime
import re
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler
import requests
import time



class Parser:

    def __init__(self, name, title, url):
        self.name = name
        self.title = title
        self.url = url
        self.videos = []
        self.videos_url = []

    def add(self, video):
        video['video'] = video['video'].replace("\r","");
        if video['video'] not in self.videos_url:
            self.videos_url.append(video['video'])
            self.videos.append(video)

def init_spider(spider):
    spider.start_urls=[]
    spider.dict_parsers = {}
    
    for parser in spider.parsers:
        print(parser.url)
        spider.start_urls.append(parser.url)
        spider.dict_parsers[parser.url] = parser
    return spider

class AssistirVideos(scrapy.Spider):

    
    name = 'assistirVideos'
    title = 'AssistirVideos Spider'
    start_urls = []
    dict_parsers = {}

    def __init__(self, *args, **kwargs):
        self.parsers = kwargs.pop('parsers', [])
        init_spider(self)
        super(AssistirVideos, *args, **kwargs)

    def parse(self, response):
        links = response.css('[itemprop="episode"] a[itemprop=url] ::attr(href)').extract()
        titles = response.css('[itemprop="episode"] span[itemprop=name] ::text').extract()
        i = 0
        parser_key = response.url
        for ep in links:
            yield scrapy.Request(response.urljoin(ep), callback=self.download,  meta={'title': titles[i], 'ep': i+1,'parser_key':parser_key})
            i += 1

    def download(self, response):
        video = response.css('video source ::attr(src)').extract_first()
        title = response.meta.get('title')
        ep = response.meta.get('ep')
        parser_key = response.meta.get('parser_key')
        parser = self.dict_parsers[parser_key]
        parser.add({'video': video, 'title': title, 'ep': ep})

    def closed(self, spider):
        write_json_parser(self)


class AnimesFox(scrapy.Spider):

    name = 'animesfoxspider'
    title = 'AnimesFox Spider'
    start_urls = []
    dict_parsers = {}

    def __init__(self, *args, **kwargs):
        self.parsers = kwargs.pop('parsers', [])
        init_spider(self)
        super(AnimesFox, *args, **kwargs)

    def parse(self, response):
        links = response.css('.lcp_catlist a ::attr(href)').extract()
        parser_key = response.url
        for ep in links:
            yield scrapy.Request(response.urljoin(ep), callback=self.download, meta={'parser_key': parser_key})

    def download(self, response):
        videos = response.css('video ::attr(src)').extract()
        title = response.css('#postitulo ::text').extract()
        ep = extract_ep_number(title[1])
        parser_key = response.meta.get('parser_key')
        for video in videos:
            if 'https://' in video:
                continue
            if 'contentId' in video and video not in self.videos:
                self.videos.append(video)
                sparser = self.dict_parsers[parser_key]
                parser.add({'video': video, 'title': title[1], 'ep': ep})

    def closed(self, spider):
        write_json_parser(self)




class Animakai(scrapy.Spider):
    name = 'animakaispider'
    title = 'AnimaKai Spider'
    start_urls = []
    dict_parsers = {}

    def __init__(self, *args, **kwargs):
        self.parsers = kwargs.pop('parsers', [])
        init_spider(self)
        super(Animakai, *args, **kwargs)

    def parse(self, response):
        links = response.css('a.thumb ::attr(href)').extract()
        titles = response.css('a.thumb ::attr(title)').extract()
        i = 0

        parser_key = response.url

        for ep in links:
            yield scrapy.Request(response.urljoin(ep), callback=self.download, meta={'title': titles[i],'parser_key': parser_key})
            i += 1

    def download(self, response):
        video = response.css('video source ::attr(src)').extract_first()
        title = response.meta.get('title')
        parser_key = response.meta.get('parser_key')
        ep = extract_ep_number(title)
        parser = self.dict_parsers[parser_key]
        parser.add({'video': video, 'title': title, 'ep': ep})

    def closed(self, spider):
        write_json_parser(self)



def extract_ep_number(title):

    numbers = [int(s) for s in re.findall(r'\b\d+\b', title)]
    
    if len(numbers) > 0:
        return int(numbers[-1])
    else:
        return 1000


def write_json_parser(spider):
    parsers = spider.parsers
    data = []
    current_date = datetime.datetime.now().strftime('%d%m%Y')
    created_date = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
    path = os.path.dirname(os.path.abspath(__file__))
    for parser in parsers:
        file_path = path + '/static/json/' + parser.name + '.json'
        videos = sort_videos(parser.videos)
        data_json = {'data': videos, 'title': parser.title,'created': created_date, 'date': current_date}
        data = json.dumps(data_json)
        file_json = open(file_path,'w')
        file_json.write(data)
        file_json.close()
        send_spider(parser.name, data_json)

def sort_videos(videos):
    return sorted(videos, key=lambda v: v['ep'], reverse=True)


def send_spider(id, data):

    headers = {'content-type': 'application/json'}
    url = 'http://video-scrap.herokuapp.com/api/v1/spider/' + str(id)
    requests.post(url, headers=headers, data=json.dumps(data))



def run_all():
    process = CrawlerProcess(get_project_settings())

    dragonBallZKayParser = Parser('dragonballkayspider',
    'Dragon Ball Kay',
    'https://www.animakai.info/anime-dublado/dragon-ball-z-kai')
    
    dragonBallZKaySagaBooParser = Parser('dragonballkayboospider',
        'Dragon Ball Kay - SAGA boo',
        'https://www.animakai.info/anime/dragon-ball-kai-2014-legendado')

    dragonBallSuperParser = Parser('dragonballsuperspider',
        'Dragon Ball Super',
        'https://www.animakai.info/anime/1589356')

    attackOnTitan2Parser = Parser('attackontitan2apider',
        'Attack On Titan 2',
        'https://www.animakai.info/anime/shingeki-no-kyojin-2')
    
    borutoParser = Parser('borutospider',
        'Boruto Next Generations',
        'https://www.animakai.info/anime/boruto-naruto-next-generations')

    animakaiParsers = [dragonBallZKayParser,dragonBallZKaySagaBooParser,dragonBallSuperParser,attackOnTitan2Parser,borutoParser]

    animakai = Animakai(parsers=animakaiParsers)
    process.crawl(animakai)


    scorpion3Parser = Parser('scorpion3spider',
        'Scorpion 3 Temporada',
        'http://assistirvideo.org/2016/10/assistir-scorpion-3-temporada-online.html')
    assistirVideosParsers = [scorpion3Parser]

    process.crawl(AssistirVideos,parsers=assistirVideosParsers)

    process.start()


run_all()