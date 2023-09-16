from domain.entities.tokenizedarticle import TokenizedArticle
from domain.entities.tokenizedcorpus import TokenizedCorpus


class MarkKeywordOnCorpus:

    def __init__(self, keywords):
        self.separator = "_"

        combined_keywords_dict = {}
        largest_level = -1
        for equalKeywords in keywords:
            for keyword in equalKeywords.items:
                key = len(keyword.split(self.separator))
                if key > largest_level:
                    largest_level = key
                if not (key in combined_keywords_dict):
                    combined_keywords_dict[key] = []
                keyword_buckets = combined_keywords_dict[key]
                keyword_buckets.append(keyword)
        self.combined_keywords_dict = combined_keywords_dict
        self.largest_level = largest_level

    def execute(self, tokenized_corpus: TokenizedCorpus):
        combined_keywords_dict = self.combined_keywords_dict
        largest_level = self.largest_level
        for level in reversed(range(largest_level+1)):
            if not (level in combined_keywords_dict):
                continue

            for tokenized_article in tokenized_corpus.tokenized_articles:
                for tokenized_sentence in tokenized_article.tokenized_sentences:
                    self.markSentence(level, tokenized_sentence)

    def markSentence(self, level, tokenized_sentence):
        current_index = 0
        keyword_buckets = self.combined_keywords_dict[level]
        while current_index < len(tokenized_sentence):
            current_keyword = self.separator.join(
                tokenized_sentence[current_index:current_index+level])
            if current_keyword in keyword_buckets:
                tokenized_sentence[current_index] = current_keyword
                del tokenized_sentence[current_index +
                                       1:current_index+level]
                pass
            current_index += 1
