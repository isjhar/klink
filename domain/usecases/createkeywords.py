from domain.entities.keyword import Keyword
from domain.repositories.csvreader import CsvReader
from domain.usecases.preprocesskeyword import PreprocessKeyword


class CreateKeywords:
    def __init__(self, csv_reader: CsvReader) -> None:
        self.csv_reader = csv_reader
        self.preprocess_keyword = PreprocessKeyword()

    def execute(self, file_name) -> list:
        rows = self.csv_reader.read(file_name)
        keywords = []
        for i, row in enumerate(rows):
            keyword = row[0]
            keyword = self.preprocess_keyword.execute(keyword)
            keyword = Keyword([keyword])
            keywords.append(keyword)
        return keywords
