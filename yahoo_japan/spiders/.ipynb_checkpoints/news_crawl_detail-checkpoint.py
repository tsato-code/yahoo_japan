# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yahoo_japan.items import YahooJapanNewsDetailItem
from scrapy_splash import SplashRequest


class NewsCrawlDetailSpider(CrawlSpider):
    name = 'news_crawl_detail'
    allowed_domains = ['yahoo.co.jp']
    start_urls = ['http://news.yahoo.co.jp/']
    # クロールするリンクを指定
    # LinkExtractor で選択された要素内のリンクをクロール
    # follow はリンク先ページに含まれているリンクをクロールするか bool デフォルトで follow=True
    # callback でリンク先を処理する関数
    # callback を指定しないと follow=False となりそれ以上リンクをたどらない
    rules = (
        Rule(
            LinkExtractor(restrict_css='ul.yjnHeader_sub_cat'),
        ),
        Rule(
            LinkExtractor(restrict_css='ul.topicsList_main li.topicsListItem'),
            callback='parse_item'
            # callback='parse_start_url'  # 2019-06-06
        )
    )
    
    def parse_start_url(self, response):
        """print("= "*20)
        print(type(response))
        print(dir(response))
        print(response.url)
        print(response._url)
        prin("= "*20)
        yield self.parse_item(response)
        return SplashRequest(
            self.start_urls[0],
            callback=self.parse_item(response),
            args={'wait':0.1}            
        )"""

    def parse_item(self, response):
        item = YahooJapanNewsDetailItem()
        item['url'] = response.url
        item['title'] = response.css('div.tpcNews_header h2::text').extract_first()
        item['category'] = response.css('ul#gnSec li.current a::text').extract_first()
        # item['num_comments'] = response.css('div#socialComments').extract()
        # print("= "*20)
        # print(response.css('div#socialComments').extract())
        # print(response.css('div#yComments ::text').extract())
        # print(response.css('div.newscomment-plugin').extract())
        # print("= "*20)
        return item
