import scrapy
from scrapy.crawler import CrawlerProcess
import json
import os
import datetime
import re
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from apscheduler.schedulers.twisted import TwistedScheduler


class Scorpion3(scrapy.Spider):

    name = 'scorpion3spider'
    title = 'Scorpion 3 Temporada'
    start_urls = ['http://assistirvideo.com/2016/10/assistir-scorpion-3-temporada-online.html']
    eps = []
    videos = []

    def parse(self, response):
        links = response.css('[itemprop="episode"] a[itemprop=url] ::attr(href)').extract()
        titles = response.css('[itemprop="episode"] span[itemprop=name] ::text').extract()
        i = 0
        for ep in links:
            yield scrapy.Request(response.urljoin(ep), callback=self.download,  meta={'title': titles[i], 'ep': i+1})
            i += 1

    def download(self, response):
        video = response.css('video source ::attr(src)').extract_first()
        title = response.meta.get('title')
        ep = response.meta.get('ep')
        if video not in self.videos:
            self.videos.append(video)
            self.eps.append({'video': video, 'title': title, 'ep': ep})

    def closed(self, spider):
        write_json_spider(self)


class DragonBallSuperSpider(scrapy.Spider):

    name = 'dragonballsuperspider'
    title = 'Dragon Ball Super'
    start_urls = ['https://www.animesfox-br.com.br/159198.html']
    eps = []
    videos = []

    def parse(self, response):
        links = response.css('.lcp_catlist a ::attr(href)').extract()
        for ep in links:
            yield scrapy.Request(response.urljoin(ep), callback=self.download)

    def download(self, response):
        videos = response.css('video ::attr(src)').extract()
        title = response.css('#postitulo ::text').extract()
        ep = extract_ep_number(title)

        for video in videos:
            if 'contentId' in video and video not in self.videos:
                self.videos.append(video)
                self.eps.append({'video': video, 'title': title[1], 'ep': ep}) 

    def closed(self, spider):
        write_json_spider(self)

class NarutoShippudenSpider(scrapy.Spider):

    name = 'narutoshippudenspider'
    title = 'Naruto Shippuden'
    start_urls = ['http://www.animesfox-br.com.br/150794.html']
    eps = []
    videos = []

    def parse(self, response):
        links = response.css('.lcp_catlist a ::attr(href)').extract()
        for ep in links:
            yield scrapy.Request(response.urljoin(ep), callback=self.download)

    def download(self, response):
        videos = response.css('video ::attr(src)').extract()
        title = response.css('#postitulo ::text').extract()
        ep = extract_ep_number(title)

        for video in videos:
            if 'https://' in video:
                continue
            if 'contentId' in video and video not in self.videos:
                self.videos.append(video)
                self.eps.append({'video': video, 'title': title[1], 'ep': ep}) 

    def closed(self, spider):
        write_json_spider(self)


def extract_ep_number(title):
    numbers = [int(s) for s in re.findall(r'\b\d+\b', title[1])]
    
    if len(numbers) > 0:
        return numbers[-1]
    else:
        return 1000


def write_json_spider(spider):
    sorted_eps = sorted(spider.eps, key=lambda k: k['ep'], reverse=True)
    path = os.path.dirname(os.path.abspath(__file__))

    file_path = path + '/static/json/' + spider.name + '.json'
    
    isfile = False
    if os.path.isfile(file_path):
        isfile = True
        with open(file_path, 'r') as current_file_json:
            current_data = json.loads(current_file_json.read())
        current_file_json.close()

    data = []

    has_new = False
    current_date = datetime.datetime.now().strftime('%d%m%Y')

    for ep in sorted_eps:
        if isfile and ep in current_data['data'] and current_data['date'] == current_date:
            ep['new'] = False
        else:
            has_new = True
            ep['new'] = True

        data.append(ep)

    data_json = {'data': data, 'has_new': has_new, 'title': spider.title, 'created': datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), 'date': current_date}
    
    data = json.dumps(data_json)

    file_json = open(file_path,'w')
    file_json.write(data)
    file_json.close()


def run_all():
    process = CrawlerProcess(get_project_settings())

    process.crawl(DragonBallSuperSpider)
    process.crawl(Scorpion3)
    process.crawl(NarutoShippudenSpider)
    process.start()





process = CrawlerProcess(get_project_settings())
sched = TwistedScheduler()
sched.add_job(process.crawl, 'cron', args=[DragonBallSuperSpider], day_of_week='sun-mon', hour='*')
sched.add_job(process.crawl, 'cron', args=[Scorpion3], day_of_week='sun-mon', hour='*')

sched.start()
process.start(False)
