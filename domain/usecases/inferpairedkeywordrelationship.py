from domain.entities.keyword import Keyword
from domain.entities.relationship import Relationship
from domain.repositories.cooccurancematrix import CooccuranceMatrix
from domain.repositories.wordembedding import WordEmbedding
from domain.usecases.equalrelationship import EqualRelationship
from domain.usecases.hierarchicalrelationshipstrength import HierarchicalRelationshipStrength


class InferPairedKeywordRelationship:
    def __init__(self, word_embedding: WordEmbedding,
                 cooccurance_matrix: CooccuranceMatrix,
                 cooccurance_matrix_by_year: dict,
                 year: int,
                 token_debut: dict,
                 sub_class_of_relationship: dict,
                 hirearchical_threshold: float,
                 temporal_hirearchical_threshold: float,
                 equal_threshold: float,
                 gamma: int,
                 wsa: float,
                 wsub: float):
        self.hirearchical_threshold = hirearchical_threshold
        self.temporal_hirearchical_threshold = temporal_hirearchical_threshold
        self.equal_threshold = equal_threshold
        self.year = year
        self.token_debut = token_debut
        self.hierarchical_relationship_strength = HierarchicalRelationshipStrength(
            word_embedding, cooccurance_matrix)
        self.wsa = wsa
        self.wsub = wsub
        self.gamma = gamma
        self.equal_relationship = EqualRelationship(
            word_embedding, cooccurance_matrix, sub_class_of_relationship)
        if year in cooccurance_matrix_by_year:
            self.temporal_hierarchical_relationship_strength = HierarchicalRelationshipStrength(
                word_embedding, cooccurance_matrix_by_year[year])

    def execute(self, keyword1, keyword2) -> Relationship:
        hierarchical_relationship_strength_value = self.hierarchical_relationship_strength.execute(
            keyword1, keyword2)
        if hierarchical_relationship_strength_value > self.hirearchical_threshold:
            return Relationship.HIERACHICAL

        equal_relationship_value = self.equal_relationship.execute(
            keyword1, keyword2, wsa=self.wsa, wsub=self.wsub)
        if equal_relationship_value > self.equal_threshold:
            return Relationship.EQUAL

        keyword1_weight = self.get_temporal_weight(keyword1, gamma=self.gamma)
        keyword2_weight = self.get_temporal_weight(keyword2, gamma=self.gamma)

        if self.temporal_hierarchical_relationship_strength != None:
            temporal_hierarchical_relationship_strength_value = self.temporal_hierarchical_relationship_strength.execute(
                keyword1, keyword2, keyword1_weight, keyword2_weight)

            if temporal_hierarchical_relationship_strength_value > self.temporal_hirearchical_threshold:
                return Relationship.HIERACHICAL

        # print("compare {} -> {} :::: hierarchical: {}, equal: {}, temporal: {}".format(keyword1, keyword2,
        #                                                                                hierarchical_relationship_strength_value,
        #                                                                                equal_relationship_value, temporal_hierarchical_relationship_strength_value))

        return Relationship.NONE

    def get_temporal_weight(self, keyword: Keyword, gamma: int):
        debut = self.getDebut(keyword)
        denominator = pow(debut - self.year, gamma)
        if denominator == 0:
            return 0
        return 1 / denominator

    def getDebut(self, keyword: Keyword):
        debut = self.year
        for item in keyword.items:
            if item in self.token_debut:
                current_debut = self.token_debut[item]
                if current_debut < debut:
                    debut = current_debut
        return debut
