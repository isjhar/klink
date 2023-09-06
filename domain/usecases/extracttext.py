from domain.usecases.stem import Stem
from domain.usecases.tokenize import Tokenize


class ExtractText:
    def __init__(self, sent_tokenizer, tokenizer):        
        self.tokenize = Tokenize(tokenizer)
        self.sent_tokenizer = sent_tokenizer
    def execute(self, text):
        sentenceResult = []
        sentences = self.sent_tokenizer.tokenize(text)
        for sentence in sentences:
            tokenResult = [];
            tokens = self.tokenize.execute(sentence)        
            for token in tokens:
                tokenResult.append(token)
            sentenceResult.append(tokenResult)
        return sentenceResult