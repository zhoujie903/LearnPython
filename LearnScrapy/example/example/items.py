# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    name = Field()
    price = Field()
    #authors = Field(serializer = lambda x: '|'.join(x))

class ForeignBookItem(BookItem):
    translator = Field()


class ExampleItem(Item):

    # x 有两个元数据，a是个字符串 
    x = Field(a='hello', b=[1, 2, 3])

    # y 有一个元数据，a是个函数 
    y = Field(a=lambda x: x ** 2)


