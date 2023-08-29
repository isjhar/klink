from domain.usecases.extracttext import ExtractText


class ProcessCooccurance:
    def __init__(self, sent_tokenizer, tokenizer, stemmer, cooccurance_counter):
        self.extract_text = ExtractText(sent_tokenizer=sent_tokenizer, stemmer=stemmer, tokenizer=tokenizer)
        self.cooccurance_counter = cooccurance_counter
    def execute(self, text):
        tokenizedSentences = self.extract_text.execute(text)
        self.cooccurance_counter.process(tokenizedSentences)