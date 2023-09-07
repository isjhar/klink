import gensim

from domain.repositories.wordembedding import WordEmbedding

class Word2VecWordEmbbedding(WordEmbedding):
    def __init__(self, tokenized_sentences) -> None:
        self.model = gensim.models.Word2Vec(tokenized_sentences, min_count = 1, vector_size=50, window = 5, sg = 1)     
        self.index = self.model.wv.key_to_index
    def similarity(self, word1, word2):        
        if word1 not in self.index or word2 not in self.index:
            return 0
        return self.model.wv.similarity(word1, word2)