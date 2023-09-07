from domain.repositories.tokenizer import Tokenizer


class Tokenize:
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
    def execute(self, text):
        return self.tokenizer.tokenize(text)