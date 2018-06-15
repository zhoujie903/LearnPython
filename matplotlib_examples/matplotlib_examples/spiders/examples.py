# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from ..items import ExampleItem


class ExamplesSpider(scrapy.Spider):
    name = 'examples'
    allowed_domains = ['matplotblib.org']
    start_urls = ['https://matplotlib.org/examples/index.html']

    

    def parse(self, response):
        le = LinkExtractor(restrict_css='div.toctree-wrapper.compound', deny='/index.html$')
        for link in le.extract_links(response):
            # print(link.url)
            yield scrapy.Request(link.url, callback=self.parse_example, dont_filter = True)


    def parse_example(self, response): 
        href = response.css('a.reference.external::attr(href)').extract_first()
        url = response.urljoin(href)
        print(url)
        example = ExampleItem()
        example['file_urls'] = [url]
        return example


