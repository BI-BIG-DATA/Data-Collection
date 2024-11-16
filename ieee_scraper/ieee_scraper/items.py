# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IEEEArticle(scrapy.Item):
    journal = scrapy.Field()
    indexation = scrapy.Field()
    publication = scrapy.Field()
    doi = scrapy.Field()
    titre = scrapy.Field()
    chercheurs = scrapy.Field()
    laboratoires = scrapy.Field()
    abstract = scrapy.Field()
    keywords = scrapy.Field()
    pays = scrapy.Field()
    quartile = scrapy.Field()
