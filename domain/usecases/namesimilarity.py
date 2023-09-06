class NameSimilarity:
    def __init__(self, tokenizer, stemmer):
        self.tokenizer=tokenizer
        self.stemmer= stemmer

    def execute(self, keyword1Tokens, keyword2Tokens):
        totalIdenticalWords =self.calculateIdenticalWords(keyword1Tokens, keyword2Tokens)
        return totalIdenticalWords / (len(keyword1Tokens) + len(keyword2Tokens)) * 2
    
    def calculateIdenticalWords(self, keyword1Tokens, keyword2Tokens):
        total = 0
        for keyword in keyword1Tokens:
            if keyword in keyword2Tokens:
                total += 1
        return total
    