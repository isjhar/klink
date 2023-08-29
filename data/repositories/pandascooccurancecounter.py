from domain.repositories.cooccurancecounter import CooccuranceCounter
import pandas as pd

class PandasCooccuranceCounter(CooccuranceCounter):
    def process(self, keywords, tokenizedSentences):    
        data = []
        for tokenizedSentence in tokenizedSentences:
            for i, token in enumerate(tokenizedSentence[:-1]):
                token2 = tokenizedSentence[i+1]
                if token in keywords and token2 in keywords:
                    data.append([token, token2])
                
        df = pd.DataFrame(data, columns=["t1", "t2"])
        co_mat = pd.crosstab(df.t1, df.t2)
        print(co_mat)
        
                