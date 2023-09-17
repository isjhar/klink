from domain.entities.keyword import Keyword
from domain.repositories.cooccurancematrix import CooccuranceMatrix
from domain.repositories.wordembedding import WordEmbedding


class EqualRelationship:
    def __init__(self, word_embedding: WordEmbedding, cooccurance_matrix: CooccuranceMatrix, sub_class_of_relationship: dict):
        self.word_embedding = word_embedding
        self.cooccurance_matrix = cooccurance_matrix
        self.sub_class_of_relationship = sub_class_of_relationship

    def execute(self, keyword1: Keyword, keyword2: Keyword, wsa=0.2, wsub=0.2):
        probability_k1_k2 = self.cooccurance_matrix.getPairedKeywordProbability(
            keyword1, keyword2)
        probability_k2_k1 = self.cooccurance_matrix.getPairedKeywordProbability(
            keyword2, keyword1)
        similarity = self.word_embedding.similarity(
            keyword1.items[0], keyword2.items[0])
        similaritySuperArea = self.calculateAverageSimilaritySuperArea(
            keyword1, keyword2)
        return similarity - wsa * similaritySuperArea - wsub * abs(probability_k1_k2 - probability_k2_k1)

    def calculateAverageSimilaritySuperArea(self, keyword1: Keyword, keyword2: Keyword):
        subClassOfKeyword1 = []
        if str(keyword1) in self.sub_class_of_relationship:
            subClassOfKeyword1 = self.sub_class_of_relationship[str(keyword1)]

        subClassOfKeyword2 = []
        if str(keyword2) in self.sub_class_of_relationship:
            subClassOfKeyword2 = self.sub_class_of_relationship[str(keyword2)]

        total_similarity = 0
        total = 0
        for superKeyword1 in subClassOfKeyword1:
            for superKeyword2 in subClassOfKeyword2:
                total_similarity += self.word_embedding.similarity(
                    superKeyword1.items[0], superKeyword2.items[0])
                total += 1
        if total == 0:
            return 0
        return total_similarity / total
