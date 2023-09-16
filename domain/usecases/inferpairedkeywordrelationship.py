from domain.entities.keyword import Keyword
from domain.entities.relationship import Relationship
from domain.repositories.cooccurancematrix import CooccuranceMatrix
from domain.repositories.wordembedding import WordEmbedding
from domain.usecases.equalrelationship import EqualRelationship
from domain.usecases.hierarchicalrelationshipstrength import HierarchicalRelationshipStrength


class InferPairedKeywordRelationship:
    def __init__(self, word_embedding: WordEmbedding, cooccurance_matrix: CooccuranceMatrix, cooccurance_matrix_by_year: dict, year: int, token_debut: dict):
        self.word_embedding = word_embedding
        self.cooccurance_matrix = cooccurance_matrix
        self.cooccurance_matrix_temporal = cooccurance_matrix_by_year[year]
        self.hirearchical_threshold = 0.2
        self.temporal_hirearchical_threshold = 0.2
        self.equal_threshold = 0.75
        self.year = year
        self.token_debut = token_debut
        self.hierarchical_relationship_strength = HierarchicalRelationshipStrength(
            self.word_embedding, self.cooccurance_matrix)
        self.equal_relationship = EqualRelationship(
            self.word_embedding, self.cooccurance_matrix)
        self.temporal_hierarchical_relationship_strength = HierarchicalRelationshipStrength(
            self.word_embedding, self.cooccurance_matrix_temporal)

    def execute(self, keyword1, keyword2) -> Relationship:
        hierarchical_relationship_strength_value = self.hierarchical_relationship_strength.execute(
            keyword1, keyword2)
        if hierarchical_relationship_strength_value > self.hirearchical_threshold:
            return Relationship.HIERACHICAL

        equal_relationship_value = self.equal_relationship.execute(
            keyword1, keyword2)
        if equal_relationship_value > self.equal_threshold:
            return Relationship.EQUAL

        keyword1_weight = self.get_temporal_weight(keyword1)
        keyword2_weight = self.get_temporal_weight(keyword2)
        temporal_hierarchical_relationship_strength_value = self.temporal_hierarchical_relationship_strength.execute(
            keyword1, keyword2, keyword1_weight, keyword2_weight)

        if temporal_hierarchical_relationship_strength_value > self.temporal_hirearchical_threshold:
            return Relationship.HIERACHICAL

        return Relationship.NONE

    def get_temporal_weight(self, keyword: Keyword, gamma=2):
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
