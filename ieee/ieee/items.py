# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IeeeItem(scrapy.Item):
    journal = scrapy.Field()
    indexation = scrapy.Field(default="IEEE")
    doi = scrapy.Field()
    titre = scrapy.Field()
    chercheurs = scrapy.Field()
    abstract = scrapy.Field()
    date = scrapy.Field()