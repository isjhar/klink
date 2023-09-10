class MarkKeywordOnSentences: 

    def __init__(self):
        self.separator = "_"
        pass
    def execute(self, keywords, tokenized_sentences):
        results = tokenized_sentences.copy()
        combined_keywords_dict = {}
        largest_level = -1
        for equalKeywords in keywords:            
            for keyword in equalKeywords.items:
                key = len(keyword.split(self.separator))
                if key > largest_level:
                    largest_level = key
                if not (key in combined_keywords_dict):
                    combined_keywords_dict[key] = []
                keyword_buckets = combined_keywords_dict[key]
                keyword_buckets.append(keyword)

        
        for level in reversed(range(largest_level+1)):
            if not (level in combined_keywords_dict):
                continue
            keyword_buckets = combined_keywords_dict[level]            
            
            for tokenized_sentence in results:
                current_index = 0
                while current_index < len(tokenized_sentence):                
                    current_keyword = self.separator.join(tokenized_sentence[current_index:current_index+level])
                    if current_keyword in keyword_buckets:                    
                        tokenized_sentence[current_index] = current_keyword       
                        del tokenized_sentence[current_index+1:current_index+level]                 
                        pass
                    current_index += 1 
                            

        return results