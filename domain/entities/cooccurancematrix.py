from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class CooccuranceMatrix:
    def __init__(self, cooccurance_matrix):
        self.cooccurance_matrix = cooccurance_matrix
        print(self.cooccurance_matrix)

    def getHierarchicalRelationShipStrength(self, keyword1, keyword2):
        probabilityK1K2 = self.getPairedKeywordProbability(keyword1,keyword2)
        probabilityK2K1 = self.getPairedKeywordProbability(keyword2, keyword1)
        similarity = self.getSimilarity(keyword1, keyword2)
        return (probabilityK2K1 - probabilityK1K2) * similarity
    

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
    
    def getSimilarity(self, keyword1, keyword2):
        if keyword1 not in self.cooccurance_matrix.index or keyword2 not in self.cooccurance_matrix.index:
            return 0
        data = []
        data.append(self.cooccurance_matrix.loc[keyword1].to_numpy())
        data.append(self.cooccurance_matrix.loc[keyword2].to_numpy())
        df = pd.DataFrame(data, columns=self.cooccurance_matrix.loc[keyword1].index)                     
        return cosine_similarity(data)[0,1]