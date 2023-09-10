from data.repositories.nltksenttokenizer import NltkSentTokenizer
from data.repositories.nltkstemmer import NltkStemmer
from data.repositories.nltktokenizer import NltkTokenizer
from data.repositories.pandascooccurancecounter import PandasCooccuranceCounter
from data.repositories.word2vecwordembedding import Word2VecWordEmbbedding
from domain.entities.keyword import Keyword
from domain.usecases.extracttext import ExtractText
from domain.usecases.hierarchicalrelationshipstrength import HierarchicalRelationshipStrength
from domain.usecases.inferpairedkeywordrelationship import InferPairedKeywordRelationship
from domain.usecases.klink import Klink
from domain.usecases.markkeywordonsentences import MarkKeywordOnSentences
from domain.usecases.processcooccurance import ProcessCooccurance
from domain.usecases.senttokenize import SentTokenize



def main():
    keywords = [Keyword(["im_isjhar"]), Keyword(["from"]), Keyword(["i"]), Keyword(["work"])]
    corpus = "hello im isjhar from makassar. i work as software developer."    

    extract_text = ExtractText(NltkSentTokenizer(), NltkTokenizer())
    tokenized_sentences = extract_text.execute(corpus)

    mark_keyword_on_sentences = MarkKeywordOnSentences()
    marked_tokenized_sentences = mark_keyword_on_sentences.execute(keywords, tokenized_sentences)


    word2vec = Word2VecWordEmbbedding(marked_tokenized_sentences)
    cooccurance_counter=PandasCooccuranceCounter()
    
    klink = Klink(word2vec, cooccurance_counter)
    klink.execute(keywords, marked_tokenized_sentences)


if __name__ == "__main__":
    main()