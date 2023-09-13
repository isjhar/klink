from domain.entities.keyword import Keyword
from domain.repositories.cooccurancematrix import CooccuranceMatrix
from domain.repositories.wordembedding import WordEmbedding


class EqualRelationship:
    def __init__(self, word_embedding: WordEmbedding, cooccurance_matrix: CooccuranceMatrix):
        self.word_embedding = word_embedding
        self.cooccurance_matrix = cooccurance_matrix

    def execute(self, keyword1: Keyword, keyword2:Keyword, wsa = 0.2, wsub = 0.2):
        probability_k1_k2 = self.cooccurance_matrix.getPairedKeywordProbability(keyword1,keyword2)
        probability_k2_k1 = self.cooccurance_matrix.getPairedKeywordProbability(keyword2, keyword1)
        similarity = self.word_embedding.similarity(keyword1, keyword2)
        similaritySuperArea = 0
        return similarity - wsa * similaritySuperArea - wsub * abs(probability_k1_k2 - probability_k2_k1)