import scrapy


class HardmobSpider(scrapy.Spider):
    name = 'hardmob'
    allowed_domains = ['www.hardmob.com.br/forums/407-Promocoes']
    start_urls = ['http://www.hardmob.com.br/forums/407-Promocoes/']

    def parse(self, response):
        pass
