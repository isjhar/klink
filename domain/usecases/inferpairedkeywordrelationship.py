from domain.entities.relationship import Relationship
from domain.repositories.cooccurancematrix import CooccuranceMatrix
from domain.repositories.wordembedding import WordEmbedding
from domain.usecases.hierarchicalrelationshipstrength import HierarchicalRelationshipStrength


class InferPairedKeywordRelationship:
    def __init__(self, word_embedding: WordEmbedding, cooccurance_matrix: CooccuranceMatrix):
        self.hierarchical_relationship_Strength = HierarchicalRelationshipStrength(word_embedding, cooccurance_matrix)        
        self.hirearchical_threshold = 0.2
        self.equal_threshold = 0.75

    def execute(self, keyword1, keyword2) -> Relationship:
        hierarchical_relationship_Strength = self.hierarchical_relationship_Strength.execute(keyword1, keyword2)
        if hierarchical_relationship_Strength > self.hirearchical_threshold:
            return Relationship.HIERACHICAL
        equal_relationship = self.hierarchical_relationship_Strength.execute(keyword1, keyword2)
        if equal_relationship> self.equal_threshold:
            return Relationship.EQUAL
        return Relationship.NONE