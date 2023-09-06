class SentTokenize:
    def __init__(self, sent_tokenizer):
        self.sent_tokenizer = sent_tokenizer
    def execute(self, text):
        return self.sent_tokenizer.tokenize(text)