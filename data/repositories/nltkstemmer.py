
from domain.repositories.stemmer import Stemmer
from nltk.stem import PorterStemmer


class NltkStemmer(Stemmer):
    def __init__(self):
        self.stemmer = PorterStemmer()
    def stem(self, token):
        return self.stemmer.stem(token)      