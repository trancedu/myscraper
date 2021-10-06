import scrapy
import json
from scrapy.http import HtmlResponse


class DecryptSpider(scrapy.Spider):
    name = 'decrypt'
    allowed_domains = ['decrypt.co']
    # Send the request
    # user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    start_urls = ['https://api.decrypt.co/content-elasticsearch/posts?_minimal=true&category=news&lang=en-US&offset=4000'
                  '&order=desc&orderby=date&per_page=1000&type=post']

    def parse(self, response):
        data = json.loads(response.body)
        for item in data:
            result = HtmlResponse(url="", body=item["content"]["rendered"], encoding='utf-8')
            content = ''.join(result.css("span::text").getall()).replace('\xa0', ' ')
            output = {
                "date": item["date_gmt"],
                "title": item["title"]["rendered"],
                "link": item["link"],
                "content": content,
            }

            yield output
            pass
