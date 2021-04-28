import scrapy
import logging
from urllib.parse import urljoin

class AdrenalineForSaleSpider(scrapy.Spider):
    name = 'adrenaline_for_sale'
    allowed_domains = ['forum.adrenaline.com.br']
    start_urls = ['https://forum.adrenaline.com.br/forums/for-sale.221']

    def parse(self, response):
        topics = response.xpath('//div[@class="structItemContainer-group js-threadList"]/div')
        for topic in topics:
            topic_title = topic.xpath('.//div/div[@class="structItem-title"]/a/text()').get()
            topic_relative_url = topic.xpath('.//div/div[@class="structItem-title"]/a/@href').get()
            author = topic.xpath('.//div/div[@class="structItem-minor"]/ul/li/a/text()').get()
            author_relative_url = topic.xpath('.//div/div[@class="structItem-minor"]/ul/li[1]/a/@href').get()
            date = topic.xpath('.//div/div[@class="structItem-minor"]/ul/li[2]/a/time/@data-time').get()
            total_messages = topic.xpath('.//div[@class="structItemContainer-group js-threadList"]/div/div[3]/dl[1]/dd/text()').get()
            total_visits = topic.xpath('.//div[@class="structItemContainer-group js-threadList"]/div/div[3]/dl[2]/dd/text()').get()
            last_message_time = topic.xpath('.//div[@class="structItemContainer-group js-threadList"]/div/div[4]/a/time/@data-time').get()

            adrenaline_url = 'https://forum.adrenaline.com.br/forums/for-sale.221'

            author_absolute_url =  urljoin(adrenaline_url, author_relative_url)
            topic_absolute_url = urljoin(adrenaline_url, topic_relative_url)
            print(adrenaline_url)
            yield response.follow(
                url=topic_relative_url, 
                callback=self.parse_topic, 
                meta={
                    'topic_title': topic_title,
                    'topic_url': topic_absolute_url,
                    'author': author,
                    'author_url': author_absolute_url,
                    'creation_date': date,
                    'total_messages': total_messages,
                    'total_visits': total_visits,
                    'last_message_time': last_message_time
                })
    
    def parse_topic(self, response):
        first_post = response.xpath("(//div[@class='bbWrapper'])[1]/text()").get()
        yield {
            'topic_title': response.request.meta['topic_title'],
            'topic_url': response.request.meta['topic_url'],
            'author': response.request.meta['author'],
            'author_url': response.request.meta['author_url'],
            'creation_date': response.request.meta['creation_date'],
            'total_messages': response.request.meta['total_messages'],
            'total_visits': response.request.meta['total_visits'],
            'last_message_time': response.request.meta['last_message_time'],
            'first_post': first_post,
        }