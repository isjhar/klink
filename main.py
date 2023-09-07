from data.repositories.nltksenttokenizer import NltkSentTokenizer
from data.repositories.nltkstemmer import NltkStemmer
from data.repositories.nltktokenizer import NltkTokenizer
from data.repositories.pandascooccurancecounter import PandasCooccuranceCounter
from data.repositories.word2vecwordembedding import Word2VecWordEmbbedding
from domain.usecases.extracttext import ExtractText
from domain.usecases.hierarchicalrelationshipstrength import HierarchicalRelationShipStrength
from domain.usecases.markkeywordonsentences import MarkKeywordOnSentences
from domain.usecases.processcooccurance import ProcessCooccurance
from domain.usecases.senttokenize import SentTokenize



def main():
    keywords = ["im_isjhar", "from", "i", "work"]
    corpus = "hello im isjhar from makassar. i work as software developer."    

    extract_text = ExtractText(NltkSentTokenizer(), NltkTokenizer())
    tokenized_sentences = extract_text.execute(corpus)

    mark_keyword_on_sentences = MarkKeywordOnSentences()
    marked_tokenized_sentences = mark_keyword_on_sentences.execute(keywords, tokenized_sentences)

    processCooccurance = ProcessCooccurance(cooccurance_counter=PandasCooccuranceCounter())
    cooccurance_matrix = processCooccurance.execute(keywords, marked_tokenized_sentences)       
    word2vec = Word2VecWordEmbbedding(marked_tokenized_sentences)
    
    hierachical_relationship_strength = HierarchicalRelationShipStrength(word2vec, cooccurance_matrix)
    print(hierachical_relationship_strength.execute("im_isjhar", "from"))


if __name__ == "__main__":
    main()