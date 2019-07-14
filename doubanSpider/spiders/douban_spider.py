# -*- coding: utf-8 -*-
import scrapy
from doubanSpider.items import DoubanspiderItem


class DoubanSpiderSpider(scrapy.Spider):
	# 爬虫名字
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 入口url，传到调度器里
    start_urls = ['https://movie.douban.com/top250']
    # 默认解析方法
    def parse(self, response):
        movie_list = response.xpath('//div[@class="article"]/ol[@class="grid_view"]/li')
        # print(type(movie_list)) # <class 'scrapy.selector.unified.SelectorList'>
        for i_item in movie_list:
        	douban_item = DoubanspiderItem()
        	douban_item['serial_number'] = i_item.xpath('./div[@class="item"]//em/text()').extract_first()
        	douban_item['moive_name'] = i_item.xpath('./div[@class="item"]/div[@class="info"]/div[@class="hd"]//span[@class="title"]/text()').extract()[0]
        	p_item = i_item.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]/p[1]')
        	# string() 获取的是p标签下面的所有文本内容，包括<br>标签后面的，text()只能获取<br>标签前面的内容
       		douban_item['introduce'] = p_item.xpath('string()').extract()[0].strip().replace(u'\xa0', u' ')
        	douban_item['star'] = i_item.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract_first()
        	douban_item['evaluate'] = i_item.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[4]/text()').extract_first().replace('人评价', '')
       		douban_item['describe'] = i_item.xpath('./div[@class="item"]/div[@class="info"]/div[@class="bd"]/p[@class="quote"]/span[@class="inq"]/text()').extract_first()
        	yield douban_item # 将数据传递给ItemPipeline
        # 解析下一页规则
        next_link = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract()
        if next_link:
        	next_link = next_link[0]
        	yield scrapy.Request("https://movie.douban.com/top250"+next_link, callback=self.parse)
        
