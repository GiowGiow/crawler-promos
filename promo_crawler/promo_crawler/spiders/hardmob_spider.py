from datetime import datetime

import scrapy


class AdrenalineSpider(scrapy.Spider):
    name = "hardmob"
    start_urls = ["https://www.hardmob.com.br/forums/407-Promocoes"]
    allowed_domains = ["hardmob.com.br"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, meta={"cloudflare": True})

    def parse(self, response):
        for topic in response.css("ol#threads > li"):
            title = topic.css("a.title::text").get()
            url = topic.css("a.title::attr(href)").get()
            author = topic.css("a.username::text").get()
            author_url = topic.css("dl.threadlastpost.td > a::attr(href)").get()
            day = topic.css("dl.threadlastpost.td dd:nth-of-type(2)::text").get()
            time = topic.css(
                "dl.threadlastpost.td dd:nth-of-type(2) > span::text"
            ).get()
            now = datetime.now()
            now = now.strftime("%m/%d/%Y")
            creation_date = f"[{now}][{day}][{time}]"
            comments = topic.css("ul.threadstats.td.alt a::text").get()
            views = topic.css("ul.threadstats.td.alt li:nth-of-type(2)::text").get()
            views = views.split()[1] if views else views

            if not url:
                continue

            # Follow each topic to read the posts
            yield response.follow(
                url=url,
                callback=self.parse_topic,
                meta={
                    "topic_title": title,
                    "topic_url": url,
                    "author": author,
                    "author_url": author_url,
                    "creation_date": creation_date,
                    "comments": comments,
                    "views": views,
                    "cloudflare": True,
                },
            )

    def parse_topic(self, response):
        # Get the fist post
        yield {
            "topic_title": response.request.meta["topic_title"],
            "topic_url": response.request.meta["topic_url"],
            "author": response.request.meta["author"],
            "author_url": response.request.meta["author_url"],
            "creation_date": response.request.meta["creation_date"],
            "comments": response.request.meta["comments"],
            "views": response.request.meta["views"],
            "first_post": response.css("div.content").get(),
        }
