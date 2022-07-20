import scrapy


class AdrenalineSpider(scrapy.Spider):
    name = "adrenaline"
    adrenaline_url = "https://forum.adrenaline.com.br/forums/for-sale.221"
    allowed_domains = ["forum.adrenaline.com.br"]
    start_urls = [adrenaline_url]

    def parse(self, response) -> scrapy.http.Request:
        # Parse topics (not the fixed ones)
        for topic in response.css(
            "div.structItemContainer-group.js-threadList > div"
        ):
            title = topic.css("div.structItem-title > a::text").get()
            topic_relative_url = topic.css(
                "div.structItem-title > a::attr(href)"
            ).get()
            author = topic.css("a.username ::text").get()
            author_url = topic.css("a.username ::attr(href)").get()
            unix_time = topic.css("time::attr(data-time)").get()
            msgs = topic.css("dl.pairs.pairs--justified dd::text").get()
            visits = topic.css(
                "dl.pairs.pairs--justified.structItem-minor dd::text"
            ).get()

            if not topic_relative_url:
                continue

            # Follow each topic to read the posts
            yield response.follow(
                url=topic_relative_url,
                callback=self.parse_topic,
                meta={
                    "topic_title": title,
                    "topic_url": topic_relative_url,
                    "author": author,
                    "author_url": author_url,
                    "creation_date": unix_time,
                    "comments": msgs,
                    "views": visits,
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
            "first_post": response.css("div.bbWrapper").get(),
        }
