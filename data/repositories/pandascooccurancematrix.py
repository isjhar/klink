import pandas as pd

from domain.repositories.cooccurancematrix import CooccuranceMatrix


class PandasCooccuranceMatrix(CooccuranceMatrix):
    def __init__(self, cooccurance_matrix):
        self.cooccurance_matrix = cooccurance_matrix        

    def getPairedKeywordProbability(self, keyword1, keyword2):
        return self.getTotalPairedKeyword(keyword1, keyword2) / self.getTotalKeyword(keyword2)

    def getTotalKeyword(self, keyword):
        total_row = 0
        total_column = 0
        if keyword in self.cooccurance_matrix.index:
            total_row = self.cooccurance_matrix.loc[keyword]["total"]
        if keyword in self.cooccurance_matrix.loc["total"].index:
            total_column = self.cooccurance_matrix.loc["total"][keyword]
        return total_row+total_column

    def getTotalPairedKeyword(self, keyword1, keyword2):
        total_row = 0
        total_column = 0
        if keyword1 in self.cooccurance_matrix.index and keyword2 in self.cooccurance_matrix.loc[keyword1].index:
            total_row = self.cooccurance_matrix.loc[keyword1][keyword2]
        if keyword2 in self.cooccurance_matrix.index and keyword1 in self.cooccurance_matrix.loc[keyword2].index:
            total_column = self.cooccurance_matrix.loc[keyword2][keyword1]
        return total_row + total_column