import json

import scrapy


class PelandoSpider(scrapy.Spider):
    name = "pelando_recent"
    allowed_domains = ["www.pelando.com.br"]
    # A default query on pelando has a limit of 20 results.
    # Experimenting showed that the query limit is 50 results
    query_limit = 50

    querystring = {
        "operationName": "RecentOffersQuery",
        "variables": '{{"limit":{lim}}}'.format(lim=query_limit),
        "extensions": (
            '{"persistedQuery":{"version":1,"sha256Hash":'
            '"19589aae3492c1f462380bc215fc7662078c512e0983bfb71464606c8e20b38d"}}'
        ),
    }

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0)"
            " Gecko/20100101 Firefox/102.0"
        ),
        "Accept": "*/*",
        "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
        "Referer": "https://www.pelando.com.br/recentes",
        "content-type": "application/json",
        "Alt-Used": "www.pelando.com.br",
    }

    def start_requests(self):
        urls = ["https://www.pelando.com.br/api/graphql"]
        for url in urls:
            yield scrapy.FormRequest(
                url=url,
                method="GET",
                formdata=self.querystring,
                headers=self.headers,
                callback=self.parse,
            )

    def parse(self, response):
        resp = json.loads(response.text)
        yield from resp["data"]["public"]["recentOffers"]["edges"]
