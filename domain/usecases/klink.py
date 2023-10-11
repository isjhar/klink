from domain.entities.graph import Graph
from domain.entities.keyword import Keyword
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
        processed_keywords = [] + keywords
        tokenized_sentences = tokenized_corpus.getTokenizedSentences()
        tokenized_sentences_by_year = tokenized_corpus.getTokenizedSentencesByYear()
        token_debut = tokenized_corpus.getTokenDebut()

        sub_class_of_relationship = {}
        equal_relationship = {}
        iterasi = 0

        while iterasi == 0 or len(equal_relationship) > 0:
            iterasi += 1
            print("--start iterasi ke-{}".format(iterasi))
            equal_relationship = {}

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
                sub_class_of_relationship=sub_class_of_relationship,
                hirearchical_threshold=self.hirearchical_threshold,
                temporal_hirearchical_threshold=self.temporal_hirearchical_threshold,
                equal_threshold=self.equal_threshold,
                gamma=self.gamma,
                wsa=self.wsa,
                wsub=self.wsub)

            temporal_sub_class_of_relationship = {}

            for keyword1 in processed_keywords:
                for keyword2 in processed_keywords:
                    if keyword1 != keyword2:
                        relationship = infer_paired_keyword_relationship.execute(
                            keyword1, keyword2)

                        keyword1_key = str(keyword1)
                        keyword2_key = str(keyword2)

                        if relationship == Relationship.HIERARCHICAL:
                            if keyword1_key + keyword2_key in equal_relationship:
                                del equal_relationship[keyword1_key +
                                                       keyword2_key]
                                print("delete {} -> {} :::: equal relation",
                                      keyword1, keyword2)

                            if keyword2_key + keyword1_key in equal_relationship:
                                del equal_relationship[keyword2_key +
                                                       keyword1_key]
                                print(
                                    "delete {} -> {} :::: equal relation".format(keyword1, keyword2))

                            if keyword2 in temporal_sub_class_of_relationship and keyword1 in temporal_sub_class_of_relationship[keyword2]:
                                temporal_sub_class_of_relationship[keyword2].remove(
                                    keyword1)

                                print(
                                    "delete {} -> {} :::: hiearchical temporal relation".format(keyword2, keyword1))

                            self.insertPairedKeywordToSubClassOfRelationship(
                                keyword1, keyword2, sub_class_of_relationship)

                            print(
                                "add {} -> {} :::: hiearchical relation".format(keyword1, keyword2))

                        if relationship == Relationship.EQUAL:
                            if keyword1_key + keyword2_key in equal_relationship:
                                continue

                            if keyword2_key + keyword1_key in equal_relationship:
                                continue

                            if keyword1 in temporal_sub_class_of_relationship and keyword2 in temporal_sub_class_of_relationship[keyword1]:
                                temporal_sub_class_of_relationship[keyword1].remove(
                                    keyword2)

                                print(
                                    "delete {} -> {} :::: hiearchical temporal relation".format(keyword1, keyword2))

                            if keyword2 in temporal_sub_class_of_relationship and keyword1 in temporal_sub_class_of_relationship[keyword2]:
                                temporal_sub_class_of_relationship[keyword2].remove(
                                    keyword1)

                                print(
                                    "delete {} -> {} :::: hiearchical temporal relation".format(keyword2, keyword1))

                            equal_relationship[keyword1_key +
                                               keyword2_key] = [keyword1, keyword2]

                            print(
                                "add {} -> {} :::: equal relation".format(keyword1, keyword2))

                        if relationship == Relationship.HIERARCHICAL_TEMPORAL:
                            if keyword1_key + keyword2_key in equal_relationship:
                                continue

                            if keyword2_key + keyword1_key in equal_relationship:
                                continue

                            if keyword2 in sub_class_of_relationship and keyword1 in sub_class_of_relationship[keyword2]:
                                continue

                            if keyword1 not in temporal_sub_class_of_relationship:
                                temporal_sub_class_of_relationship[keyword1] = [
                                ]

                            temporal_sub_class_of_relationship[keyword1].append(
                                keyword2)

                            print(
                                "add {} -> {} :::: hierarchical temporal relation".format(keyword1, keyword2))

            for temporal_keyword1 in temporal_sub_class_of_relationship:
                for temporal_keyword2 in temporal_sub_class_of_relationship[temporal_keyword1]:
                    self.insertPairedKeywordToSubClassOfRelationship(
                        temporal_keyword1, temporal_keyword2, sub_class_of_relationship)

            keylist = list(equal_relationship.keys())
            for key in keylist:
                if key not in equal_relationship:
                    continue
                relationship = equal_relationship[key]
                keyword1 = relationship[0]
                keyword2 = relationship[1]

                isSubClassOfRelationSame = self.isSubClassOfRelationSame(
                    sub_class_of_relationship, keyword1, keyword2)

                if isSubClassOfRelationSame:
                    continue

                del equal_relationship[key]
                print(
                    "delete {} -> {} :::: equal relation".format(keyword1, keyword2))

            for key in equal_relationship:
                relationship = equal_relationship[key]
                keyword1 = relationship[0]
                keyword2 = relationship[1]
                print("{} --equal--> {}".format(str(keyword1), str(keyword2)))

            for keyword1 in sub_class_of_relationship:
                for keyword2 in sub_class_of_relationship[keyword1]:
                    print("{} --subclassof--> {}".format(str(keyword1), str(keyword2)))

            for key in equal_relationship:
                relationship = equal_relationship[key]
                keyword1 = self.findParentKeywords(
                    processed_keywords, relationship[0])
                keyword2 = self.findParentKeywords(
                    processed_keywords, relationship[1])

                if keyword1 is None or keyword2 is None or keyword1 == keyword2:
                    continue

                parent_keyword = keyword1
                child_keyword = keyword2
                if keyword2.isContains(keyword1):
                    parent_keyword = keyword2
                    child_keyword = keyword1

                print("{} MERGE TO {}".format(
                    str(child_keyword), str(parent_keyword)))

                for item in child_keyword.items:
                    parent_keyword.addEqualKeyword(item)

                if child_keyword in processed_keywords:
                    processed_keywords.remove(child_keyword)

            merged_sub_class_of_relationships = {}
            for keyword1 in sub_class_of_relationship:
                for keyword2 in sub_class_of_relationship[keyword1]:
                    merged_keyword1 = self.findParentKeywords(
                        processed_keywords, keyword1)
                    merged_keyword2 = self.findParentKeywords(
                        processed_keywords, keyword2)
                    if merged_keyword1 not in merged_sub_class_of_relationships:
                        merged_sub_class_of_relationships[merged_keyword1] = []
                    if merged_keyword2 in merged_sub_class_of_relationships[merged_keyword1]:
                        continue
                    if merged_keyword1 == merged_keyword2:
                        continue

                    merged_sub_class_of_relationships[merged_keyword1].append(
                        merged_keyword2)

            sub_class_of_relationship = merged_sub_class_of_relationships

            print("----------result iterasi {}".format(iterasi))
            no_relation_keywords = []
            for keyword1 in sub_class_of_relationship:
                if keyword1 not in no_relation_keywords:
                    no_relation_keywords.append(keyword1)
                keyword2s = sub_class_of_relationship[keyword1]
                for keyword2 in keyword2s:
                    if keyword2 not in no_relation_keywords:
                        no_relation_keywords.append(keyword2)
                    print("{} subclassof {}".format(
                        str(keyword1), str(keyword2)))

            print("--no relation")
            for keyword in processed_keywords:
                if keyword not in no_relation_keywords:
                    print("{}".format(keyword))

            print("--end iterasi ke-{}".format(iterasi))

        return Graph(processed_keywords, sub_class_of_relationship)

    def buildCooccuranceMatrixYear(self, keywords, tokenized_sentences_by_year: dict):
        coocurance_matrix_per_year = {}
        for year in tokenized_sentences_by_year:
            tokenized_sentences = tokenized_sentences_by_year[year]
            cooccurance_matrix = self.process_cooccurance.execute(
                keywords, tokenized_sentences)
            coocurance_matrix_per_year[year] = cooccurance_matrix
        return coocurance_matrix_per_year

    def hasEqualRelationship(self, keyword1_key: str, keyword2_key: str, equal_relationship: dict):
        return keyword1_key + keyword2_key not in equal_relationship and keyword2_key + keyword1_key not in equal_relationship

    def insertPairedKeywordToSubClassOfRelationship(self, keyword1: Keyword, keyword2: Keyword, sub_class_of_relationship):
        if keyword1 not in sub_class_of_relationship:
            sub_class_of_relationship[keyword1] = []

        if keyword2 in sub_class_of_relationship[keyword1]:
            return

        sub_class_of_relationship[keyword1].append(
            keyword2)

    def findParentKeywords(self, processed_keywords: list, keyword: Keyword):
        for processed_keyword in processed_keywords:
            if processed_keyword.isContains(keyword):
                return processed_keyword
        return None

    def isSubClassOfRelationSame(self, sub_class_of_relationship: dict, keyword1: Keyword, keyword2: Keyword):
        keyword1SubClassOfRelationships = self.getSubClassOfRelationShip(
            sub_class_of_relationship, keyword1)
        keyword2SubClassOfRelationships = self.getSubClassOfRelationShip(
            sub_class_of_relationship, keyword2)

        for keyword1SubClassOfRelationship in keyword1SubClassOfRelationships:
            isFound = False
            for keyword2SubClassOfRelationship in keyword2SubClassOfRelationships:
                if keyword1SubClassOfRelationship[0] == keyword1 and keyword2SubClassOfRelationship[0] == keyword2 and keyword1SubClassOfRelationship[1] == keyword2SubClassOfRelationship[1]:
                    isFound = True
                    break

                if keyword1SubClassOfRelationship[1] == keyword1 and keyword2SubClassOfRelationship[1] == keyword2 and keyword1SubClassOfRelationship[0] == keyword2SubClassOfRelationship[0]:
                    isFound = True
                    break

            if not isFound:
                return False
        return True

    def getSubClassOfRelationShip(self, sub_class_of_relationship: dict, keyword: Keyword):
        result = []
        for keyword1 in sub_class_of_relationship:
            for keyword2 in sub_class_of_relationship[keyword1]:
                if keyword1 == keyword or keyword2 == keyword:
                    result.append([keyword1, keyword2])

        return result
