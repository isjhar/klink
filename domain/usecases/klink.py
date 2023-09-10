from domain.entities.relationship import Relationship
from domain.repositories.cooccurancecounter import CooccuranceCounter
from domain.repositories.wordembedding import WordEmbedding
from domain.usecases.inferpairedkeywordrelationship import InferPairedKeywordRelationship
from domain.usecases.processcooccurance import ProcessCooccurance


class Klink:
    def __init__(self, word_embedding: WordEmbedding, cooccurance_counter: CooccuranceCounter):
        self.word_embedding = word_embedding
        self.process_cooccurance = ProcessCooccurance(cooccurance_counter)

    def execute(self, keywords: list, marked_tokenized_sentences: list):
        merge_keyword_exist = True
        processed_keywords = [] + keywords
        while merge_keyword_exist:
            merge_keyword_exist = False
            cooccurance_matrix = self.process_cooccurance.execute(processed_keywords, marked_tokenized_sentences)
            infer_paired_keyword_relationship = InferPairedKeywordRelationship(self.word_embedding, cooccurance_matrix)    
            for keyword1 in keywords:
                for keyword2 in keywords:
                    if keyword1 != keyword2:
                        relationship = infer_paired_keyword_relationship.execute(keyword1, keyword2)
                        if relationship ==  Relationship.EQUAL:
                           merge_keyword_exist = True 