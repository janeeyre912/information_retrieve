from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider


def my_request_processor(request, response):
    request.meta['robot'] = response.meta


class ConcordiaSpider(CrawlSpider):
    file_limit = 100
    name = "concordia"
    start_urls = [
        'https://www.concordia.ca/ginacody.html',
    ]
    robot_content = ""
    lang_attr = ""
    visited_urls = set()
    rules = (
        Rule(
            LinkExtractor(
                deny=(
                    r'^(?!https://www.concordia.ca).+',  # stay in concordia domain
                    r'^(https://www.concordia.ca/fr).+',  # don't go to french page
                    r'([A-z]+=[0-9]+)$',  # don't go over pages 9 (empty pages)
                    r'([A-z]+=[A-z]+)$',  # don't click on filters (e.g sort=title)
                ),
            ),
            callback='parse_item',
            follow=True),
    )
    docID = 0

    # obey robots.txt and robots meta tags
    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "ROBOTS_META_TAG_OBEY": True,
    }

    def parse_item(self, response):
        if self.docID >= int(self.file_limit):
            raise CloseSpider("Limit reached.")

        self.robot_content = response.xpath("//meta[@name='robots']/@content").extract_first()
        self.lang_attr = response.xpath('//html/@lang').extract_first()

        url = response.url
        if url in self.visited_urls:
            self.logger.info(f'Already scrapped: {url}')
            yield

        if self.robot_content == "" or self.robot_content == "index,follow" and self.lang_attr == "en":
            self.logger.info(f'Scrapping doc #{self.docID + 1}: {url}')
            filename = response.url.split("/")[-1]
            with open("testData/" + filename, 'wb') as f:
                f.write(response.body)

        self.docID += 1
        self.visited_urls.add((url, self.docID))
