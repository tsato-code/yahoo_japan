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
    # follow (bool) はリンク先ページに含まれているリンクをクロールするかどうか（デフォルトで follow=True）
    # callback でリンク先を処理する関数
    # callback を指定しないと follow=False となりそれ以上リンクをたどらない
    rules = (
        Rule(
            LinkExtractor(restrict_css='ul.yjnHeader_sub_cat'),
        ),
        Rule(
            LinkExtractor(restrict_css='ul.topicsList_main li.topicsListItem'),
            callback='parse_item'
        )
    )

    
    def parse_item(self, response):
        # url, title, category を取得
        item = YahooJapanNewsDetailItem()
        item['url'] = response.url
        item['title'] = response.css('div.tpcNews_header h2::text').extract_first()
        item['category'] = response.css('ul#gnSec li.current a::text').extract_first()
        return item