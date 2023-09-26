import urllib.request

from domain.repositories.filedownloader import FileDownloader


class UrlFileDownloader(FileDownloader):
    def download(self, url, path) -> list:
        urllib.request.urlretrieve(url, path)
