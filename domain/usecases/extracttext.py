from domain.entities.tokenizedarticle import TokenizedArticle
from domain.entities.tokenizedcorpus import TokenizedCorpus
from domain.repositories.senttokenizer import SentTokenizer
from domain.repositories.tokenizer import Tokenizer
from domain.usecases.tokenize import Tokenize


class ExtractText:
    def __init__(self, sent_tokenizer: SentTokenizer, tokenizer: Tokenizer):
        self.tokenize = Tokenize(tokenizer)
        self.sent_tokenizer = sent_tokenizer

    def execute(self, corpus) -> TokenizedCorpus:
        tokenized_corpus = []
        for article in corpus:
            sentences = self.sent_tokenizer.tokenize(article.text)
            tokenized_sentences = []
            for sentence in sentences:
                tokenized_sentence = []
                tokens = self.tokenize.execute(sentence)
                for token in tokens:
                    tokenized_sentence.append(token)
                tokenized_sentences.append(tokenized_sentence)
            tokenized_corpus.append(TokenizedArticle(
                article.year, tokenized_sentences))
        return TokenizedCorpus(tokenized_corpus)
