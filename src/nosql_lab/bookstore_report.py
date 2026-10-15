
#!/usr/bin/env python3

import logging
import os

import pymongo

# Read Atlas credentials from environment variables.
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Configure logging for connection status and errors.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def main():
    """Connect to Atlas and print each author's linked books."""
    # Include authors from the original files and the authors added in Case Study 1.
    author_ids = ["author_002", "author_003", "author_004"]

    client = None

    try:
        # Check that all required environment variables are available.
        if not all([MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]):
            raise ValueError("One or more MongoDB Atlas environment variables are missing.")

        # Connect to the Atlas cluster and verify the connection.
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=10000
        )
        client.admin.command("ping")
        logging.info("Successfully connected to MongoDB Atlas.")

        # Select the database and collections.
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        # Count the selected authors that exist in the database.
        author_count = authors.count_documents({"_id": {"$in": author_ids}})
        print(f"Authors: {author_count}\n")

        # Find each author and then find books linked to that author.
        for author in authors.find({"_id": {"$in": author_ids}}):
            print(author["name"])

            for book in books.find({"author_ids": author["_id"]}):
                print(f"  {book['title']} ({book['published_year']})")

            print()

    except (pymongo.errors.PyMongoError, ValueError) as error:
        logging.error("Unable to generate the bookstore report: %s", error)

    finally:
        # Close the connection even if an error occurs.
        if client is not None:
            client.close()
            logging.info("MongoDB connection closed.")


if __name__ == "__main__":
    main()
