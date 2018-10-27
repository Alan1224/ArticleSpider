# -*- coding: utf-8 -*-
from urllib import parse

import scrapy
import re
from scrapy.http import Request
from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']


    def parse(self, response):
        # 解析列表中所有的url，并交给scrapy下载后并进行解析
        post_nodes = response.css(".post.floated-thumb div a")
        for post_node in post_nodes:
            post_url = post_node.css("::attr(href)").extract_first("")
            image_url = post_node.css(" img::attr(src)").extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":parse.urljoin(response.url,image_url)},callback=self.parse_detail)

        next_url = response.css(".next.page-numbers::attr(href)").extract()[0]
        if next_url:
            yield Request(url=next_url, callback=self.parse)
        pass

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()
        article_item["url"] = response.url
        article_item["url_object_id"] = get_md5(response.url)
        # 提取文章具体字段
        article_item["title"] = response.css('.entry-header h1::text').extract()[0]
        article_item["create_date"] = response.css('.entry-meta-hide-on-mobile::text').extract()[0].replace("·","").strip()
        article_item["praise_nums"] = response.css('.btn-bluet-bigger.href-style.vote-post-up.register-user-only  h10::text').extract()[0]
        article_item["front_image_url"] = [response.meta.get("front_image_url", "")]
        fav_nums = response.css('.btn-bluet-bigger.href-style.bookmark-btn.register-user-only::text').extract()[0]#收藏数
        if re.match(".*?(\d+).*",fav_nums):
            article_item["fav_nums"] = int(re.match(".*?(\d+).*",fav_nums).group(1))
        else:
            article_item["fav_nums"] = 0
        comments_nums = response.css('.btn-bluet-bigger.href-style.hide-on-480::text').extract()[0]
        if re.match(".*?(\d+).*", comments_nums):
            article_item["comments_nums"] = int(re.match(".*?(\d+).*", comments_nums).group(1))
        else:
            article_item["comments_nums"] = 0
        article_item["content"] = response.css('.entry').extract()
        article_item["tags"] = response.css('.entry-meta-hide-on-mobile a::text').extract()[0]
        article_item["author"] = response.css('.copyright-area a::text').extract()[0]

        yield article_item
