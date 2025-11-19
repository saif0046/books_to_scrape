## BooksToScrape – Web Scraping Task (Scrapy Framework)

This project is a complete Scrapy-based web scraper built to extract book information from BooksToScrape.com
It collects the following details from every book:
- Title
- Price
- Availability
- Rating

The scraped data is:
- Saved into a CSV file (books.csv)
- Stored into a SQLite database (books.db)
- Extracted with error handling, retries, pagination, and rotating User-Agents

This scraper also includes:
- Error handling
- Retry logic for failed requests
- Pagination support
- Rotating User-Agents for safer crawling


## Installation & Setup

- Create and Activate virtual environment:
```bash
$ python3 -m venv venv
$ source venv/bin/activate  # Linux / Mac
#$ venv\Scripts\activate     # Windows
```

- Install dependencies inside the virtual environment
```bash
$ pip install scrapy
```

- Navigate into the project folder:
```bash
$ cd books_to_scrape
```

- Running the spider use scrapy's command:
```bash
$ scrapy crawl books_to_scrape_spider
```
After running, the output files will appear:
- books.csv -> All scraped books in CSV format
- books.db -> SQLite database storing all book records