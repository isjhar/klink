from domain.repositories.tokenizer import Tokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
import nltk

nltk.download('punkt')

class NltkTokenizer(Tokenizer):
    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')
    def tokenize(self, text):        
        return self.tokenizer.tokenize(text)