import pandas as pd
from domain.entities.keyword import Keyword

from domain.repositories.cooccurancematrix import CooccuranceMatrix


class PandasCooccuranceMatrix(CooccuranceMatrix):
    def __init__(self, cooccurance_matrix):
        self.cooccurance_matrix = cooccurance_matrix

    def getPairedKeywordProbability(self, keyword1: Keyword, keyword2: Keyword):
        total_keyword = self.getTotalKeyword(keyword2)
        if total_keyword <= 0:
            return 0

        total_paired = self.getTotalPairedKeyword(keyword1, keyword2)
        return total_paired / total_keyword

    def getTotalKeyword(self, keyword: Keyword):
        total_row = 0
        total_column = 0
        str_keyword = str(keyword)
        if str_keyword in self.cooccurance_matrix.index:
            total_row = self.cooccurance_matrix.loc[str_keyword]["total"]
        if str_keyword in self.cooccurance_matrix.loc["total"].index:
            total_column = self.cooccurance_matrix.loc["total"][str_keyword]
        return total_row+total_column

    def getTotalPairedKeyword(self, keyword1: Keyword, keyword2: Keyword):
        total_row = 0
        total_column = 0
        str_keyword1 = str(keyword1)
        str_keyword2 = str(keyword2)
        if str_keyword1 in self.cooccurance_matrix.index and str_keyword2 in self.cooccurance_matrix.loc[str_keyword1].index:
            total_row = self.cooccurance_matrix.loc[str_keyword1][str_keyword2]
        if str_keyword2 in self.cooccurance_matrix.index and str_keyword1 in self.cooccurance_matrix.loc[str_keyword2].index:
            total_column = self.cooccurance_matrix.loc[str_keyword2][str_keyword1]
        return total_row + total_column

    def __str__(self) -> str:
        return str(self.cooccurance_matrix)
