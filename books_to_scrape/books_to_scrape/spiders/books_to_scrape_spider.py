import random
import scrapy
from books_to_scrape.items import BooksToScrapeItem


class BooksToScrapeSpiderSpider(scrapy.Spider):
    """
    Spider for scraping book information from https://books.toscrape.com.
    Includes retry logic, timeout rules, and rotating User-Agent headers.
    """
    name = "books_to_scrape_spider"
    # Custom behavior and retry rules for the spider
    custom_settings = {
        "DOWNLOAD_TIMEOUT": 15,  # Prevent request from hanging too long
        "RETRY_TIMES": 5,  # Number of retries for failed requests
        "RETRY_HTTP_CODES": [500, 502, 503, 504, 522, 524, 408, 429]
    }

    def __init__(self, *args, **kwargs):
        """
        Initialize spider settings such as allowed domains, start URLs,
        and a list of User-Agent strings for rotation.
        """
        super().__init__(*args, **kwargs)
        self.allowed_domains = ["www.tender24.de"]
        self.start_urls = ["https://books.toscrape.com"]
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
        ]

    def parse(self, response, **kwargs):
        """
        Main parsing logic. Extracts book details from the page.
        Also handles pagination and rotates User-Agent for each next page request.
        """

        if response.status != 200:
            self.logger.error(f"Website returned status {response.status}")
            return

        # Loop through each book item on the current page
        for row in response.xpath("//ol[@class='row']/li"):
            try:
                item = BooksToScrapeItem()
                item["title"] = row.xpath(".//h3/a/@title").get(default="N/A")
                item["price"] = row.xpath(".//p[@class='price_color']/text()").get(default="N/A")
                item["availability"] = (
                    row.xpath(
                        ".//div[contains(@class, 'product_price')]/p[contains(@class, 'instock availability')]/i/following::text()[1]")
                    .get(default="N/A").strip()
                )

                rating_raw = row.xpath(".//p[contains(@class, 'star-rating')]/@class").get()
                item["rating"] = rating_raw.split()[-1] if rating_raw else "N/A"
                # Send item to pipelines (CSV + DB)
                yield item

            except Exception as e:
                self.logger.error(f"Error parsing book item: {e}")

        # Handle Pagination
        next_pagination_href_available = response.xpath(
            "//li[contains(@class, 'next')]/a/@href"
        ).get()
        if next_pagination_href_available:
            next_pagination_url = response.urljoin(next_pagination_href_available)
            # Send request for next pagination with a random User-Agent
            yield scrapy.Request(
                url=next_pagination_url,
                headers={"User-Agent": random.choice(self.user_agents)},
                callback=self.parse,
                dont_filter=True # Allows visiting same URL
            )
