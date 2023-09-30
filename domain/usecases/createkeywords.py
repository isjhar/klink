from domain.entities.keyword import Keyword
from domain.repositories.csvreader import CsvReader


class CreateKeywords:
    def __init__(self, csv_reader: CsvReader) -> None:
        self.csv_reader = csv_reader
        pass

    def execute(self, file_name) -> list:
        rows = self.csv_reader.read(file_name)
        keywords = []
        for i, row in enumerate(rows):
            keyword = row[0]
            keyword = keyword.replace(" ", "_")
            keyword = Keyword([keyword])
            keywords.append(keyword)
        return keywords
