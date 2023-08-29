from domain.usecases.stem import Stem
from domain.usecases.tokenize import Tokenize


class ExtractText:
    def __init__(self, sent_tokenizer, tokenizer, stemmer):        
        self.tokenize = Tokenize(tokenizer)
        self.stem = Stem(stemmer)
        self.sent_tokenizer = sent_tokenizer
    def execute(self, text):
        sentenceResult = []
        sentences = self.sent_tokenizer.tokenize(text)
        for sentence in sentences:
            tokenResult = [];
            tokens = self.tokenize.execute(sentence)        
            for token in tokens:
                tokenResult.append(self.stem.execute(token))
            sentenceResult.append(tokenResult)
        return sentenceResult