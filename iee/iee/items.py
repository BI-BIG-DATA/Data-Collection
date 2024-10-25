# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IeeItem(scrapy.Item):
    'title': scrapy.Field()
    'authors':scrapy.Field()
    'abstract':scrapy.Field()
    'country':scrapy.Field()
    'date_pub':scrapy.Field()
    'journal':scrapy.Field()
    'topic':scrapy.Field()
    'latitude':scrapy.Field()
    'longitude':scrapy.Field()
