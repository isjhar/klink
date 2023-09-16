class TokenizedCorpus:
    def __init__(self, tokenized_articles: list) -> None:
        self.tokenized_articles = tokenized_articles

    def getTokenizedSentences(self) -> list:
        tokenized_sentences = []
        for tokenized_article in self.tokenized_articles:
            tokenized_sentences += tokenized_article.tokenized_sentences
        return tokenized_sentences

    def getTokenizedSentencesByYear(self) -> dict:
        sentences_per_year = {}
        for tokenized_article in self.tokenized_articles:
            if tokenized_article.year not in sentences_per_year:
                sentences_per_year[tokenized_article.year] = []
            sentences_per_year[tokenized_article.year] += tokenized_article.tokenized_sentences
        return sentences_per_year

    def getTokenDebut(self) -> dict:
        token_debut = {}
        for tokenized_article in self.tokenized_articles:
            for tokenized_sentence in tokenized_article.tokenized_sentences:
                for token in tokenized_sentence:
                    if token not in token_debut:
                        token_debut[token] = 9999999

                    current_year = token_debut[token]
                    if tokenized_article.year < current_year:
                        token_debut[token] = tokenized_article.year
        return token_debut
