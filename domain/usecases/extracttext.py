from domain.repositories.senttokenizer import SentTokenizer
from domain.repositories.tokenizer import Tokenizer
from domain.usecases.stem import Stem
from domain.usecases.tokenize import Tokenize


class ExtractText:
    def __init__(self, sent_tokenizer: SentTokenizer, tokenizer: Tokenizer):        
        self.tokenize = Tokenize(tokenizer)
        self.sent_tokenizer = sent_tokenizer
        
    def execute(self, text):
        tokenized_sentences = []
        sentences = self.sent_tokenizer.tokenize(text)
        for sentence in sentences:
            tokenized_sentence = [];
            tokens = self.tokenize.execute(sentence)        
            for token in tokens:
                tokenized_sentence.append(token)
            tokenized_sentences.append(tokenized_sentence)
        return tokenized_sentences