import scrapy
from ieee.items import IeeeItem
from urllib.parse import quote
from scrapy_splash import SplashRequest

class IeeeSpider(scrapy.Spider):
    name = "ieee"
    allowed_domains = ["ieeexplore.ieee.org"]
    
    def __init__(self, query="machine learning", num_pages=5, *args, **kwargs):
        super(IeeeSpider, self).__init__(*args, **kwargs)
        self.query = quote(query)
        self.num_pages = int(num_pages)

    def start_requests(self):
        url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={self.query}&language=fr"
        yield SplashRequest(url, self.parse, args={'wait': 3})

    def parse(self, response):
        # Parse article links on the main page
        articles = response.css('.List-results-items')
        for article in articles:
            relative_url = article.css('h3.text-md-md-lh a::attr(href)').get()
            if relative_url:
                article_url = response.urljoin(relative_url)
                
                # Open each article page with Splash
                yield SplashRequest(article_url, self.parse_article, args={'wait': 3})

        # Handle pagination
        next_page = response.css('a.pagination__btn--next::attr(href)').get()
        if next_page and self.num_pages > 1:
            self.num_pages -= 1
            next_page_url = response.urljoin(next_page)
            yield SplashRequest(next_page_url, self.parse, args={'wait': 3})

    def parse_article(self, response):
        # Parse detailed information from the article page
        item = IeeeItem(
            journal=response.css('div.stats-document-abstract-doi a::text').get(),
            doi=response.css('div.stats-document-abstract-doi a::text').get(),
            titre=response.css('h1.document-title span::text').get(),
            chercheurs=", ".join(response.css('div.authors-info-container a span::text').getall()),
            laboratoires=", ".join(response.css('div.author-affiliations span::text').getall()),
            abstract=" ".join(response.css('div.abstract-text p::text').getall()),
            date=response.css('div.publisher-info-container span::text').re_first(r'\d{4}')
        )
        yield item
