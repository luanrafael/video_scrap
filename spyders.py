import scrapy
from scrapy.crawler import CrawlerProcess
import json
import os
import datetime
import re
from scrapy.utils.log import configure_logging

class Scorpion3(scrapy.Spider):

    name = 'scorpion3spider'
    title = 'Scorpion 3 Temporada'
    start_urls = ['http://assistirvideo.com/2016/10/assistir-scorpion-3-temporada-online.html']
    eps = []

    def __init__(self):
        configure_logging({'LOG_FILE' : self.name + ".log"})

    def parse(self, response):
        links = response.css('[itemprop="episode"] a[itemprop=url] ::attr(href)').extract()
        print("***LINKS****")
        print(links)
        titles = response.css('[itemprop="episode"] span[itemprop=name] ::text').extract()
        print("***TITULOS****")
        print(titles)
        i = 0
        for ep in links:
            yield scrapy.Request(response.urljoin(ep), callback=self.download,  meta={'title': titles[i], 'ep': i+1})
            i += 1

    def download(self, response):
        video = response.css('video source ::attr(src)').extract_first()
        title = response.meta.get('title')
        ep = response.meta.get('ep')
        print("#### VIDEO ###")
        print(video)
        print("#### TITULO ###")
        print(title)
        self.eps.append({'video': video, 'title': title, 'ep': ep})

    def closed(self, spider):
        sorted_eps = sorted(self.eps, key=lambda k: k['ep'], reverse=True) 
        path = os.path.dirname(os.path.abspath(__file__))

        data_json = {'data': sorted_eps, 'title': self.title, 'created': datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}
        
        data = json.dumps(data_json)

        file_json = open(path + '/static/json/' + self.name + '.json','w')
        file_json.write(data)
        file_json.close()

#

class DragonBallSuperSpider(scrapy.Spider):

    name = 'dragonballsuperspider'
    title = 'Dragon Ball Super'
    start_urls = ['https://www.animesfox-br.com.br/159198.html']
    eps = []

    def __init__(self):
        configure_logging({'LOG_FILE' : self.name + ".log"})

    def parse(self, response):
        links = response.css('.lcp_catlist a ::attr(href)').extract()
        for ep in links:
            yield scrapy.Request(response.urljoin(ep), callback=self.download)

    def download(self, response):
        videos = response.css('video ::attr(src)').extract()
        title = response.css('#postitulo ::text').extract()
        ep = [int(s) for s in re.findall(r'\b\d+\b', title[1])][-1]
        for video in videos:
            if 'contentId' in video:
                self.eps.append({'video': video, 'title': title[1], 'ep': ep}) 

    def closed(self, spider):
        sorted_eps = sorted(self.eps, key=lambda k: k['ep'], reverse=True)
        path = os.path.dirname(os.path.abspath(__file__))

        data_json = {'data': sorted_eps, 'title': self.title, 'created': datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}
        
        data = json.dumps(data_json)

        file_json = open(path + '/static/json/' + self.name + '.json','w')
        file_json.write(data)
        file_json.close()

class NarutoShippudenSpider(scrapy.Spider):

    name = 'narutoshippudenspider'
    title = 'Naruto Shippuden'
    start_urls = ['http://www.animesfox-br.com.br/150794.html']
    eps = []

    def __init__(self):
        configure_logging({'LOG_FILE' : self.name + ".log"})

    def parse(self, response):
        links = response.css('.lcp_catlist a ::attr(href)').extract()
        for ep in links:
            yield scrapy.Request(response.urljoin(ep), callback=self.download)

    def download(self, response):
        videos = response.css('video ::attr(src)').extract()
        title = response.css('#postitulo ::text').extract()
        ep = [int(s) for s in re.findall(r'\b\d+\b', title[1])][-1]
        for video in videos:
            if 'contentId' in video:
                self.eps.append({'video': video, 'title': title[1], 'ep': ep}) 

    def closed(self, spider):
        sorted_eps = sorted(self.eps, key=lambda k: k['ep'], reverse=True)
        path = os.path.dirname(os.path.abspath(__file__))

        data_json = {'data': sorted_eps, 'title': self.title, 'created': datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}
        
        data = json.dumps(data_json)

        file_json = open(path + '/static/json/' + self.name + '.json','w')
        file_json.write(data)
        file_json.close()


def run_all():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(DragonBallSuperSpider)
    process.crawl(Scorpion3)
    process.crawl(NarutoShippudenSpider)
    process.start()


 
run_all()