# -*- coding: utf-8 -*-
import scrapy
from ScrapyTest.items import ScrapytestItem
#DoubanSpiderSpider继承自scrapy.Spider
class DoubanSpiderSpider(scrapy.Spider):
    #这里是爬虫名称
    name = 'douban_spider'
    #允许的域名
    allowed_domains = ['movie.douban.com']
    #入口URL，放入调度器
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        #循环电影的条目
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']//li")
        for i_item in movie_list:
            douban_item = ScrapytestItem()
            #写详细的数据解析
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(".//div[@class='item']/div[@class='info']"
                                                     "/div[@class='hd']/a/span[@class='title'][1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='bd']/p[1]/text()").extract()
            #数据的处理，去除空格、换行
            for i_content in content:
                content_s = "".join(i_content.split())
                douban_item['introduce'] = content_s
            douban_item['evaluate'] = i_item.xpath(".//span[@class = 'rating_num']/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
            #yield到pipeline中
            yield douban_item
        #解析下一页规则，取后页的Xpath
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request('http://movie.douban.com/top250'+next_link,callback=self.parse)