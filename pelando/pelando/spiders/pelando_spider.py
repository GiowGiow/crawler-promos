import scrapy


class PelandoSpiderSpider(scrapy.Spider):
    name = 'pelando_spider'
    allowed_domains = ['www.pelando.com.br/recentes?page=1']
    start_urls = ['https://www.pelando.com.br/recentes?page=1/']

    def parse(self, response):
        deals = response.xpath('//div[@class="threadGrid"]')
        for deal in deals:
            image = deal.xpath('.//div[contains(@class, "threadGrid-image")]/a/img/@src').get()
            rating  = deal.xpath('.//div[contains(@class, "threadGrid-headerMeta")]/div[1]/div[1]/span/text()').get()
            name = deal.xpath('.//div[contains(@class, "threadGrid-title")]/strong/a/text()').get()
            link = deal.xpath('.//div[contains(@class, "threadGrid-title")]/strong/a/@href').get()
            price = deal.xpath('.//div[contains(@class, "threadGrid-title")]/span/span[1]/span/text()').get()
            store_link_pelando = deal.xpath('.//div[contains(@class, "threadGrid-title")]/span/a/@href').get()
            store_name = deal.xpath('.//div[contains(@class, "threadGrid-title")]/span/a/span/span/text()').get()
            deal_link = deal.xpath('.//div[contains(@class, "threadGrid-body")]/div/div/a/@href').get()
            deal_link2 = deal.xpath('.//div[contains(@class, "threadGrid-footerMeta")]/div/span[3]/a/@href').get()
            deal_cupom = deal.xpath('.//div[contains(@class, "threadGrid-body")]/div/div/div/div/input/@value').get()
            description = deal.xpath('.//div[contains(@class, "threadGrid-body")]/div[2]/div/div/text()').get()
            author = deal.xpath('.//div[contains(@class, "threadGrid-footerMeta")]/div/span/span/button[2]/span/text()').get()

            if link == deal_link or deal_link == None:
                deal_link = deal_link2

            yield {
                'image': image,
                'rating': rating,
                'name': name,
                'link': link,
                'price': price,
                'store_link_pelando': store_link_pelando,
                'store_name': store_name,
                'deal_link': deal_link,
                'deal_cupom': deal_cupom,
                'description': description,
                'author': author
            }