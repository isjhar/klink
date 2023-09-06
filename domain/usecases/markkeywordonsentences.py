class MarkKeywordOnSentences: 

    def __init__(self):
        self.separator = "_"
        pass
    def execute(self, keywords, tokenizedSentences):
        combinedKeywordsDict = {}
        largestLevel = -1
        for keyword in keywords:            
            key = len(keyword)
            if key > largestLevel:
                largestLevel = key
            if not (key in combinedKeywordsDict):
                combinedKeywordsDict[key] = []
            keywordBuckets = combinedKeywordsDict[key]
            keywordBuckets.append(self.separator.join(keyword))

        print(combinedKeywordsDict)
        
        for level in reversed(range(largestLevel+1)):
            if not (level in combinedKeywordsDict):
                continue
            keywordBuckets = combinedKeywordsDict[level]            
            
            for tokenizedSentence in tokenizedSentences:
                currentIndex = 0
                while currentIndex < len(tokenizedSentence):                
                    currentKeyword = self.separator.join(tokenizedSentence[currentIndex:currentIndex+level])
                    if currentKeyword in keywordBuckets:                    
                        tokenizedSentence[currentIndex] = currentKeyword       
                        del tokenizedSentence[currentIndex+1:currentIndex+level]                 
                        pass
                    currentIndex += 1 
                            

        print(tokenizedSentences)