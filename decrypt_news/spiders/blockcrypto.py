import json
import scrapy
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
import random


class BlockcryptoSpider(scrapy.Spider):
    # def __init__(self, user_agent=""):
    #     self.user_agent = user_agent
    #
    #     self.ua_list = [
    #         "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    #         "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    #         "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    #         "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    #         "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    #         "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    #         "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    #         "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    #         "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    #         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    #         "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0", ]
    def __init__(self):
        super().__init__()
        self.offset = 0

    def process_request(self, request, spider):
        ua = random.choice(self.ua_list)
        request.headers.setdefault('Use-Agent', ua)

    name = 'blockcrypto'
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    # allowed_domains = ['x.com']
    start_urls = ['https://www.theblockcrypto.com/api/get/posts?offset=130&post_type=post,linked,daily&posts_per_page=10&v=5688721658742']

    def parse(self, response):
        data = json.loads(response.body)
        if "payload" not in data:
            self.offset += 10
            next_page = f'https://www.theblockcrypto.com/api/get/posts?offset={self.offset}&post_type=daily&posts_per_page=10'
            yield response.follow(next_page, callback=self.parse)
            return
        yield from data["payload"]["posts"]
        self.offset = self.offset + 10
        next_page = f'https://www.theblockcrypto.com/api/get/posts?offset={self.offset}&post_type=daily&posts_per_page=10'
        if self.offset < 10 * 100:
            yield response.follow(next_page, callback=self.parse)
        # data = json.loads(response.body)
        # url = data["payload"]["posts"][0]["url"]
        # title = data["payload"]["posts"][0]["title"]
        # # date is EDT
        # date = data["payload"]["posts"][0]["published"]
        # content = data["payload"]["posts"][0]["body"] # need to extract
        # label = data["payload"]["posts"][0]["label"]
        # excerpt = data["payload"]["posts"][0]["excerpt"]
        # body = data["payload"]["posts"][0]["body"]
        # content = ''.join(Selector(text=body).css("p::text").getall())
        #
        # for item in data:
        #
        #     result = HtmlResponse(url="", body=item["content"]["rendered"], encoding='utf-8')
        #     content = ''.join(result.css("span::text").getall()).replace('\xa0', ' ')
        #     output = {
        #         "date": item["date_gmt"],
        #         "title": item["title"]["rendered"],
        #         "link": item["link"],
        #         "content": content,
        #     }


