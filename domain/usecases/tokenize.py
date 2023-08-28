class Tokenize:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    def execute(self, text):
        return self.tokenizer.tokenize(text)