from domain.entities.article import Article
from domain.repositories.csvreader import CsvReader
from domain.repositories.filedownloader import FileDownloader
from domain.repositories.pdfreader import PdfReader


class CreateCorpus:
    def __init__(self, csv_reader: CsvReader, file_downloader: FileDownloader, pdf_reader: PdfReader) -> None:
        self.csv_reader = csv_reader
        self.file_downloader = file_downloader
        self.pdf_reader = pdf_reader
        pass

    def execute(self, file_name) -> list:
        rows = self.csv_reader.read(file_name)
        corpus = []
        for i, row in enumerate(rows):
            year = row[0]
            url = row[1]
            pdf_file_name = "{}.pdf".format(i)
            self.file_downloader.download(url, pdf_file_name)
            text = self.pdf_reader.read(pdf_file_name)
            article = Article(year, text.lower())
            corpus.append(article)
        return corpus
