from data.repositories.pandascooccurancematrix import PandasCooccuranceMatrix
from domain.repositories.cooccurancecounter import CooccuranceCounter
import pandas as pd

from domain.repositories.cooccurancematrix import CooccuranceMatrix

class PandasCooccuranceCounter(CooccuranceCounter):
    def process(self, keywords, marked_tokenized_sentences) -> CooccuranceMatrix:    
        paired_keywords = []
        for k1, keyword1 in enumerate(keywords):
            for k2, keyword2 in enumerate(keywords):
                if k1 != k2:
                    paired_keywords.append([keyword1, keyword2])
                

        data = []        
        for marked_tokenized_sentence in marked_tokenized_sentences:
            for i, token in enumerate(marked_tokenized_sentence[:-2]):
                paired_token = marked_tokenized_sentence[i:i+2]
                for paired_keyword in paired_keywords:
                    if self.isPairedTokenEqual(paired_token, paired_keyword):
                        keyword1 = str(paired_keyword[0])
                        keyword2 = str(paired_keyword[1])
                        data.append([keyword1, keyword2])
                                        
        df = pd.DataFrame(data, columns=["t1", "t2"])
        co_mat = pd.crosstab(df.t1, df.t2, margins=True, margins_name='total')
        return PandasCooccuranceMatrix(cooccurance_matrix=co_mat)

    def isPairedTokenEqual(self, paired_token, paired_keyword):
        if len(paired_token) < 2 or len(paired_keyword) < 2:
            return False        
        return paired_token[0] in paired_keyword[0].items and paired_token[1] in paired_keyword[1].items
                