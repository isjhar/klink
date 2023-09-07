from domain.repositories.cooccurancematrix import CooccuranceMatrix
from domain.repositories.wordembedding import WordEmbedding


class HierarchicalRelationShipStrength:
    def __init__(self, word_embedding: WordEmbedding, cooccurance_matrix: CooccuranceMatrix):
        self.word_embedding = word_embedding
        self.cooccurance_matrix = cooccurance_matrix

    def execute(self, keyword1, keyword2):
        probabilityK1K2 = self.cooccurance_matrix.getPairedKeywordProbability(keyword1,keyword2)
        probabilityK2K1 = self.cooccurance_matrix.getPairedKeywordProbability(keyword2, keyword1)
        similarity = self.word_embedding.similarity(keyword1, keyword2)
        return (probabilityK2K1 - probabilityK1K2) * similarity * (1 + self.calculateIdenticalWords(keyword1, keyword2))
    
    def calculateIdenticalWords(self, keyword1, keyword2):
        total = 0
        keyword1_tokens = keyword1.split("_")
        keyword2_tokens = keyword2.split("_")
        for keyword in keyword1_tokens:
            if keyword in keyword2_tokens:
                total += 1
        return total
