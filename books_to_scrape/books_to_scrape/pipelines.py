from itemadapter import ItemAdapter
import csv
import sqlite3
import logging


class BookCsvPipeline:
    """
    Pipeline to save scraped data into a CSV file.
    """

    def open_spider(self, spider):
        """Initialize the CSV file when the spider opens."""
        try:
            self.file = open("books.csv", "w", newline="", encoding="utf-8")
            self.writer = csv.writer(self.file)

            # Write header row
            self.writer.writerow(["Title", "Price", "Availability", "Rating"])
            logging.info("CSV file created successfully.")

        except Exception as e:
            logging.error(f"Error opening CSV file: {e}")

    def process_item(self, item, spider):
        """Write each scraped item into the CSV file."""
        try:
            adapter = ItemAdapter(item)
            self.writer.writerow([
                adapter.get("title", "N/A"),
                adapter.get("price", "N/A"),
                adapter.get("availability", "N/A"),
                adapter.get("rating", "N/A"),
            ])
        except Exception as e:
            logging.error(f"Error writing to CSV: {e}")

        return item

    def close_spider(self, spider):
        """Close the CSV file when spider finishes."""
        self.file.close()
        logging.info("CSV file closed.")



class BookDatabasePipeline:
    """
    Pipeline to save scraped book data into a SQLite database.
    """

    def open_spider(self, spider):
        """Connect to the database and create table if not exists."""
        try:
            self.connection = sqlite3.connect("books.db")
            self.cursor = self.connection.cursor()

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    price TEXT,
                    availability TEXT,
                    rating TEXT
                )
            """)
            self.connection.commit()
            logging.info("Database connected and table is ready.")

        except Exception as e:
            logging.error(f"Database connection error: {e}")

    def process_item(self, item, spider):
        """Insert each scraped item into the SQLite table."""
        try:
            adapter = ItemAdapter(item)

            self.cursor.execute("""
                INSERT INTO books (title, price, availability, rating)
                VALUES (?, ?, ?, ?)
            """, (
                adapter.get("title", "N/A"),
                adapter.get("price", "N/A"),
                adapter.get("availability", "N/A"),
                adapter.get("rating", "N/A"),
            ))

            self.connection.commit()

        except Exception as e:
            logging.error(f"Error inserting item into database: {e}")

        return item

    def close_spider(self, spider):
        """Close the database connection."""
        self.connection.close()
        logging.info("Database connection closed.")
