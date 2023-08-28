from nltk.tokenize import sent_tokenize

from domain.repositories.senttokenizer import SentTokenizer


class NltkSentTokenizer(SentTokenizer):    
    def tokenize(self, text):        
        return sent_tokenize(text)