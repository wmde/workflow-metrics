import csv

from author.author import Author
from author.author_factory import AuthorFactory

class AccountDataListLoader:
    def load_author_data_from_csv_file(self, filename: str) -> dict[str, Author]:
        author_data = {}
        author_factory = AuthorFactory()
        with open(filename) as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                author = author_factory.create_from_data_dict(row)
                author_data[author.author_id] = author

        return author_data