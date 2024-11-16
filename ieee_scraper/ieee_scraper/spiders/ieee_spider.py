import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import quote
import logging
from ieee_scraper.items import IEEEArticle  # Make sure items.py is correctly set up with IEEEArticle

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class IEEEScrapySpider(scrapy.Spider):
    name = "ieee_scrapy"
    allowed_domains = ["ieeexplore.ieee.org"]
    start_urls = []

    def __init__(self, query="blockchain", num_pages=5, *args, **kwargs):
        super(IEEEScrapySpider, self).__init__(*args, **kwargs)
        encoded_query = quote(query)
        self.start_urls = [f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={encoded_query}"]
        self.num_pages = num_pages
        self.results = []

    def parse(self, response):
        logging.info("Processing IEEE page")

        # Parse each article in the list
        articles = response.css('div.List-results-items')
        for article in articles:
            title = article.css('.fw-bold::text').get()
            article_url = article.css('.fw-bold::attr(href)').get()
            
            if article_url:
                yield response.follow(
                    article_url,
                    callback=self.parse_article,
                    meta={'title': title}
                )
        
        # Follow pagination
        next_page = response.css('button.stats-Pagination_Next_11:not([disabled])::attr(data-page-number)').get()
        if next_page and int(next_page) <= self.num_pages:
            next_page_url = response.urljoin(f"?pageNumber={next_page}")
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_article(self, response):
        logging.info("Parsing IEEE article details")

        article = IEEEArticle(
            journal=response.css('.text-md-md-lh::text').get(default=""),
            indexation='IEEE',
            publication=response.css('.text-base-md-lh.publisher-info-container.black-tooltip::text').get(default=""),
            doi=response.css('.u-pb-1.stats-document-abstract-doi::text').get(default=""),
            titre=response.meta['title'],
            chercheurs=response.css('.authors-info-container.overflow-ellipsis.text-base-md-lh.authors-minimized::text').get(default=""),
            laboratoires=response.css('.author-affiliations::text').get(default=""),
            abstract=response.css('div[xplmathjax]::text').get(default=""),
            keywords=response.css('.doc-keywords-list.stats-keywords-list::text').getall(),
            pays='',
            quartile=''
        )

        yield article

    def closed(self, reason):
        logging.info("Spider closed: %s", reason)

# Uncomment the following to run this spider as a standalone script
# if __name__ == "__main__":
#     process = CrawlerProcess()
#     process.crawl(IEEEScrapySpider, query="blockchain", num_pages=5)
#     process.start()
