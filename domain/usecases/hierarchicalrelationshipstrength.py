from domain.entities.keyword import Keyword
from domain.repositories.cooccurancematrix import CooccuranceMatrix
from domain.repositories.wordembedding import WordEmbedding


class HierarchicalRelationshipStrength:
    def __init__(self, word_embedding: WordEmbedding, cooccurance_matrix: CooccuranceMatrix):
        self.word_embedding = word_embedding
        self.cooccurance_matrix = cooccurance_matrix

    def execute(self, keyword1: Keyword, keyword2: Keyword, keyword1_weight=1, keyword2_weight=1):
        probability_k1_k2 = keyword1_weight * self.cooccurance_matrix.getPairedKeywordProbability(
            keyword1, keyword2)
        probability_k2_k1 = keyword2_weight * self.cooccurance_matrix.getPairedKeywordProbability(
            keyword2, keyword1)
        similarity = self.word_embedding.similarity(keyword1, keyword2)
        return (probability_k2_k1 - probability_k1_k2) * similarity * (1 + self.name_similarity(keyword1, keyword2))

    def name_similarity(self, keyword1: Keyword, keyword2: Keyword):
        max = -9999999
        for item1 in keyword1.items:
            for item2 in keyword2.items:
                name_similarity = self.calculate_name_similarity(item1, item2)
                if (name_similarity > max):
                    max = name_similarity
        return max

    def calculate_name_similarity(self, keyword1, keyword2):
        total = 0
        keyword1_tokens = keyword1.split("_")
        keyword2_tokens = keyword2.split("_")
        for keyword in keyword1_tokens:
            if keyword in keyword2_tokens:
                total += 1
        return total / (len((keyword1_tokens)) + len((keyword2_tokens))) * 2
