from data.repositories.pandascooccurancematrix import PandasCooccuranceMatrix
from domain.repositories.cooccurancecounter import CooccuranceCounter
import pandas as pd

from domain.repositories.cooccurancematrix import CooccuranceMatrix

class PandasCooccuranceCounter(CooccuranceCounter):
    def process(self, keywords, marked_tokenized_sentences) -> CooccuranceMatrix:    
        combinedKeywords = []
        for k1, keyword1 in enumerate(keywords):
            for k2, keyword2 in enumerate(keywords):
                if k1 != k2:
                    combinedKeywords.append([keyword1, keyword2])
                

        data = []        
        for markedTokenizedSentence in marked_tokenized_sentences:
            for i, token in enumerate(markedTokenizedSentence[:-2]):
                tokens = markedTokenizedSentence[i:i+2]
                for combinedKeyword in combinedKeywords:
                    if self.isKeywordsEqual(tokens, combinedKeyword):
                        data.append([combinedKeyword[0], combinedKeyword[1]])
                                        
        df = pd.DataFrame(data, columns=["t1", "t2"])
        co_mat = pd.crosstab(df.t1, df.t2, margins=True, margins_name='total')
        return PandasCooccuranceMatrix(cooccurance_matrix=co_mat)

    def isKeywordsEqual(self, tokens, combined_keywords):        
        for i, token in enumerate(tokens):
            if token != combined_keywords[i]:
                return False
        return True
                