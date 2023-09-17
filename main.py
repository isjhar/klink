from data.repositories.nltksenttokenizer import NltkSentTokenizer
from data.repositories.nltkstemmer import NltkStemmer
from data.repositories.nltktokenizer import NltkTokenizer
from data.repositories.pandascooccurancecounter import PandasCooccuranceCounter
from data.repositories.word2vecwordembedding import Word2VecWordEmbbedding
from domain.entities.article import Article
from domain.entities.keyword import Keyword
from domain.usecases.extracttext import ExtractText
from domain.usecases.hierarchicalrelationshipstrength import HierarchicalRelationshipStrength
from domain.usecases.inferpairedkeywordrelationship import InferPairedKeywordRelationship
from domain.usecases.klink import Klink
from domain.usecases.markkeywordoncorpus import MarkKeywordOnCorpus
from domain.usecases.processcooccurance import ProcessCooccurance
from domain.usecases.senttokenize import SentTokenize


def main():
    keywords = [Keyword(["im_isjhar"]), Keyword(["from"]),
                Keyword(["i"]), Keyword(["work"]),
                Keyword(["im_abdul"])]
    corpus = [Article(2020, "hello im abdul from bandung. my role as tester. i work at pt digital solution"),
              Article(
                  2020, "hello im isjhar from indonesia. i work at pt jaringan mega komputasi"),
              Article(
                  2021, "hello im isjhar from makassar. my role as software engineering"),
              Article(2021, "i work as software developer."),]

    extract_text = ExtractText(NltkSentTokenizer(), NltkTokenizer())
    tokenized_corpus = extract_text.execute(corpus)

    mark_keyword_on_corpus = MarkKeywordOnCorpus(keywords)
    mark_keyword_on_corpus.execute(tokenized_corpus)

    word2vec = Word2VecWordEmbbedding(
        tokenized_corpus.getTokenizedSentences())

    cooccurance_counter = PandasCooccuranceCounter()

    klink = Klink(word_embedding=word2vec,
                  cooccurance_counter=cooccurance_counter, year=2021)
    klink.execute(keywords, tokenized_corpus)


if __name__ == "__main__":
    main()
