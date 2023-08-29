from domain.repositories.cooccurancecounter import CooccuranceCounter
import pandas as pd

class PandasCooccuranceCounter(CooccuranceCounter):
    def process(self, keywords, tokenizedSentences):    
        combinedKeywordsDict = {}
        for k1, keyword1 in enumerate(keywords):
            for k2, keyword2 in enumerate(keywords):
                if k1 != k2:
                    key = len(keyword1) + len(keyword2)
                    if not (key in combinedKeywordsDict):
                        combinedKeywordsDict[key] = []
                    keywordBuckets = combinedKeywordsDict[key]
                    keywordBuckets.append([keyword1, keyword2])
        
        print(combinedKeywordsDict)

        data = []
        for level in combinedKeywordsDict:
            combinedKeywords = combinedKeywordsDict[level]            
            for tokenizedSentence in tokenizedSentences:
                for i, token in enumerate(tokenizedSentence[:-level]):
                    tokens = tokenizedSentence[i:i+level]
                    for combinedKeyword in combinedKeywords:
                        if self.isKeywordsEqual(tokens, combinedKeyword):
                            data.append([" ".join(combinedKeyword[0]), " ".join(combinedKeyword[1])])
                        
                
        df = pd.DataFrame(data, columns=["t1", "t2"])
        co_mat = pd.crosstab(df.t1, df.t2)
        print(df)    

    def isKeywordsEqual(self, tokens, combinedKeywords):
        concatedKeywords = combinedKeywords[0] + combinedKeywords[1]
        if len(tokens) != len(concatedKeywords):
            return False
        for i, token in enumerate(tokens):
            if token != concatedKeywords[i]:
                return False
        return True
                