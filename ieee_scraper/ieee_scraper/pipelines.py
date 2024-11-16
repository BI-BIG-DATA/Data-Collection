# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# class IeeeScraperPipeline:
#     def process_item(self, item, spider):
#         return item
import pandas as pd
import json

class IEEEPipeline:
    def open_spider(self, spider):
        self.results = []

    def close_spider(self, spider):
        df = pd.DataFrame([item for item in self.results])
        df.to_csv("ieee_results.csv", index=False, encoding="utf-8")

        with open("ieee_results.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)

    def process_item(self, item, spider):
        self.results.append(dict(item))
        return item
