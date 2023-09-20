from domain.entities.relationship import Relationship
from domain.entities.tokenizedcorpus import TokenizedCorpus
from domain.repositories.cooccurancecounter import CooccuranceCounter
from domain.repositories.wordembedding import WordEmbedding
from domain.usecases.inferpairedkeywordrelationship import InferPairedKeywordRelationship
from domain.usecases.processcooccurance import ProcessCooccurance


class Klink:
    def __init__(self, word_embedding: WordEmbedding, cooccurance_counter: CooccuranceCounter, year):
        self.word_embedding = word_embedding
        self.process_cooccurance = ProcessCooccurance(cooccurance_counter)
        self.year = year

    def execute(self, keywords: list, tokenized_corpus: TokenizedCorpus):
        merge_keyword_exist = True
        processed_keywords = [] + keywords
        tokenized_sentences = tokenized_corpus.getTokenizedSentences()
        tokenized_sentences_by_year = tokenized_corpus.getTokenizedSentencesByYear()
        token_debut = tokenized_corpus.getTokenDebut()

        subClassOfRelationship = {}

        while merge_keyword_exist:
            merge_keyword_exist = False
            cooccurance_matrix = self.process_cooccurance.execute(
                processed_keywords, tokenized_sentences)
            cooccurance_matrix_by_year = self.buildCooccuranceMatrixYear(
                processed_keywords, tokenized_sentences_by_year)

            infer_paired_keyword_relationship = InferPairedKeywordRelationship(
                self.word_embedding,
                cooccurance_matrix,
                cooccurance_matrix_by_year,
                year=self.year,
                token_debut=token_debut,
                sub_class_of_relationship=subClassOfRelationship)

            equal_relationship = {}
            sub_class_of_relationship = {}

            for keyword1 in processed_keywords:
                for keyword2 in processed_keywords:
                    if keyword1 != keyword2:
                        relationship = infer_paired_keyword_relationship.execute(
                            keyword1, keyword2)

                        if relationship == Relationship.EQUAL:
                            merge_keyword_exist = True
                            keyword1_key = str(keyword1)
                            keyword2_key = str(keyword2)
                            if keyword1_key + keyword2_key not in equal_relationship or keyword2_key + keyword1_key not in equal_relationship:
                                equal_relationship[keyword1_key +
                                                   keyword2_key] = [keyword1, keyword2]

                        if relationship == Relationship.HIERACHICAL:
                            if keyword1_key + keyword2_key in equal_relationship:
                                del equal_relationship[keyword1_key +
                                                       keyword2_key]
                            if keyword2_key + keyword1_key in equal_relationship:
                                del equal_relationship[keyword2_key +
                                                       keyword1_key]

                            keyword1_key = str(keyword1)
                            if keyword1_key not in sub_class_of_relationship:
                                sub_class_of_relationship[keyword1_key] = []
                            sub_class_of_relationship[keyword1_key].append(
                                keyword2)

            for key in equal_relationship:
                relationship = equal_relationship[key]
                keyword1 = relationship[0]
                keyword2 = relationship[1]
                for item in keyword2.items:
                    keyword1.add_equal_keyword(item)
                processed_keywords.remove(keyword2)

        return processed_keywords, sub_class_of_relationship

    def buildCooccuranceMatrixYear(self, keywords, tokenized_sentences_by_year: dict):
        coocurance_matrix_per_year = {}
        for year in tokenized_sentences_by_year:
            tokenized_sentences = tokenized_sentences_by_year[year]
            cooccurance_matrix = self.process_cooccurance.execute(
                keywords, tokenized_sentences)
            coocurance_matrix_per_year[year] = cooccurance_matrix
        return coocurance_matrix_per_year
