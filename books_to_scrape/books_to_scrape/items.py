import scrapy


class BooksToScrapeItem(scrapy.Item):
    """
    Item class that defines the structure of the data
    we want to scrape from books.toscrape.com.
    Each field represents a column for CSV/DB.
    """
    title = scrapy.Field()
    price = scrapy.Field()
    availability = scrapy.Field()
    rating = scrapy.Field()

