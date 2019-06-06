# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from yahoo_japan.items import YahooJapanNewsItem


class NewsCrawlSpider(CrawlSpider):
    name = 'news_crawl'
    allowed_domains = ['yahoo.co.jp']
    start_urls = ['https://news.yahoo.co.jp/']
    # クロールするリンクを指定
    # LinkExtractor で選択された要素内のリンクをクロール
    rules = (
        Rule(
            LinkExtractor(restrict_css='ul.yjnHeader_sub_cat'),
            # LinkExtractor(restrict_css='div.topicsList_main'),
            # callback='parse_start_url'
            callback='parse_item'
        ),
    )

    def parse_item(self, response):
        category = response.css('ul.yjnHeader_sub_cat li.current a::text').extract_first()
        for topic in response.css('ul.topicsList_main li.topicsListItem'):
            item = YahooJapanNewsItem()
            item['headline'] = topic.css('a::text').extract_first()
            item['url'] = topic.css('a::attr(href)').extract_first()
            item['category'] = category
            yield item


    def parse_start_url(self, response):
        return self.parse_item(response)