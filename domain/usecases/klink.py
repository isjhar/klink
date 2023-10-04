from domain.entities.graph import Graph
from domain.entities.relationship import Relationship
from domain.entities.tokenizedcorpus import TokenizedCorpus
from domain.repositories.cooccurancecounter import CooccuranceCounter
from domain.repositories.wordembedding import WordEmbedding
from domain.usecases.inferpairedkeywordrelationship import InferPairedKeywordRelationship
from domain.usecases.processcooccurance import ProcessCooccurance


class Klink:
    def __init__(self, word_embedding: WordEmbedding, cooccurance_counter: CooccuranceCounter,
                 year: int,
                 hirearchical_threshold: float,
                 temporal_hirearchical_threshold: float,
                 equal_threshold: float,
                 gamma: int,
                 wsa: float,
                 wsub: float):

        self.hirearchical_threshold = hirearchical_threshold
        self.temporal_hirearchical_threshold = temporal_hirearchical_threshold
        self.equal_threshold = equal_threshold
        self.gamma = gamma
        self.wsa = wsa
        self.wsub = wsub
        self.word_embedding = word_embedding
        self.process_cooccurance = ProcessCooccurance(cooccurance_counter)
        self.year = year

    def execute(self, keywords: list, tokenized_corpus: TokenizedCorpus) -> Graph:
        merge_keyword_exist = True
        processed_keywords = [] + keywords
        tokenized_sentences = tokenized_corpus.getTokenizedSentences()
        tokenized_sentences_by_year = tokenized_corpus.getTokenizedSentencesByYear()
        token_debut = tokenized_corpus.getTokenDebut()

        subClassOfRelationship = {}
        iterasi = 0

        while merge_keyword_exist:
            iterasi += 1
            print("iterasi ke-{}".format(iterasi))
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
                sub_class_of_relationship=subClassOfRelationship,
                hirearchical_threshold=self.hirearchical_threshold,
                temporal_hirearchical_threshold=self.temporal_hirearchical_threshold,
                equal_threshold=self.equal_threshold,
                gamma=self.gamma,
                wsa=self.wsa,
                wsub=self.wsub)

            equal_relationship = {}
            sub_class_of_relationship = {}

            for keyword1 in processed_keywords:
                for keyword2 in processed_keywords:
                    if keyword1 != keyword2:
                        relationship = infer_paired_keyword_relationship.execute(
                            keyword1, keyword2)

                        print("compare {} -> {} :::: {}".format(keyword1,
                              keyword2, relationship))

                        if relationship == Relationship.EQUAL:
                            merge_keyword_exist = True
                            keyword1_key = str(keyword1)
                            keyword2_key = str(keyword2)
                            if keyword1_key + keyword2_key not in equal_relationship and keyword2_key + keyword1_key not in equal_relationship:
                                equal_relationship[keyword1_key +
                                                   keyword2_key] = [keyword1, keyword2]

                        if relationship == Relationship.HIERARCHICAL:
                            if keyword1_key + keyword2_key in equal_relationship:
                                del equal_relationship[keyword1_key +
                                                       keyword2_key]
                            if keyword2_key + keyword1_key in equal_relationship:
                                del equal_relationship[keyword2_key +
                                                       keyword1_key]

                            keyword1_key = str(keyword1)
                            if keyword1 not in sub_class_of_relationship:
                                sub_class_of_relationship[keyword1] = []
                            sub_class_of_relationship[keyword1].append(
                                keyword2)

            for key in equal_relationship:
                relationship = equal_relationship[key]
                keyword1 = relationship[0]
                keyword2 = relationship[1]
                parent_keyword = keyword1
                child_keyword = keyword2
                if keyword2.isContains(keyword1):
                    parent_keyword = keyword2
                    child_keyword = keyword1

                for item in child_keyword.items:
                    parent_keyword.addEqualKeyword(item)

                if child_keyword in processed_keywords:
                    processed_keywords.remove(child_keyword)

        return Graph(processed_keywords, sub_class_of_relationship)

    def buildCooccuranceMatrixYear(self, keywords, tokenized_sentences_by_year: dict):
        coocurance_matrix_per_year = {}
        for year in tokenized_sentences_by_year:
            tokenized_sentences = tokenized_sentences_by_year[year]
            cooccurance_matrix = self.process_cooccurance.execute(
                keywords, tokenized_sentences)
            coocurance_matrix_per_year[year] = cooccurance_matrix
        return coocurance_matrix_per_year
