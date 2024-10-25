import scrapy
from items import IeeItem
from scrapy_splash import SplashRequest

class IeeSpider(scrapy.Spider):
    name = "iee"
    topic = "None"

    ITEM_PIPELINES = {
        'myproject.pipelines.PricePipeline': 300,
        'myproject.pipelines.JsonWriterPipeline': 800,
    }

    def __init__(self, keywords=None, topic=None, *args, **kwargs):
        super(IeeSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={keywords}"]
        self.topic = topic

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2})

    def parse(self, response):
        for article in response.css('a::attr(href)'):
            # For each article, go to article details, new request, get response, parse store
            yield {
                'title': article.css('a.result-list-title-link').extract_first()
            }
            yield SplashRequest('https://ieeexplore.ieee.org' + article.extract(), self.parse_article, args={'wait': 3})

        # For next page in response
        for next_page in response.css('a.next::attr("href")'):
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        item = IeeItem()

        # Response contains the article details page
        title = response.css('.document-title').css('span::text').extract_first()
        authors = response.css('.authors-info').css('span').css('a').css('span::text').extract()

        affiliation_name = response.css('.affiliation_name::text').extract_first() if response.css('.affiliation_name::text').extract_first() is not None else ""
        affiliation_city = response.css('.affiliation_city::text').extract_first() if response.css('.affiliation_city::text').extract_first() is not None else ""
        affiliation_country = response.css('.affiliation_country::text').extract_first() if response.css('.affiliation_country::text').extract_first() is not None else "USA"

        abstract = response.css('.abstract-desktop-div-sections').css('div').css('div::text').extract()
        location = response.css('.abstract-conferenceLoc::text').extract()
        pub_year = response.css('.stats-document-abstract-publishedIn').css('a::text').extract()

        item['title'] = title
        item['authors'] = ', '.join(authors)
        item['abstract'] = ', '.join(abstract)
        item['location'] = ', '.join(location.extract())
        item['date_pub'] = pub_year.extract().split(' ')[0]
        item['topic'] = self.topic
        item['latitude'] = 0
        item['longitude'] = 0
        item['journal'] = ', '.join(pub_year.extract()).split(' ')[1:]

        yield item
