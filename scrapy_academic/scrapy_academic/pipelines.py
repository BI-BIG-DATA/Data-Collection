# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter

class ScrapyAcademicPipeline:
    def __init__(self):
        # Replace `<your-cluster-url>` with your actual cluster connection URL
        self.client = pymongo.MongoClient(
            "mongodb+srv://<user>:<password>@cluster0.ghz8l.mongodb.net/"
        )
        self.db = self.client['sample_mflix']
        self.collection = self.db['data']

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Check if the document already exists based on unique fields (e.g., 'doi' or 'titre')
        query = {
            "$or": [
                {"doi": adapter.get('doi')},
                {"titre": adapter.get('titre')}
            ]
        }

        if not self.collection.find_one(query):
            # Insert only if the document does not already exist
            self.collection.insert_one(adapter.asdict())
            spider.logger.info("New item inserted.")
        else:
            spider.logger.info("Duplicate item found: Skipping insertion.")

        return item

    def close_spider(self, spider):
        self.client.close()

