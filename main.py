from data.repositories.nltksenttokenizer import NltkSentTokenizer
from data.repositories.nltkstemmer import NltkStemmer
from data.repositories.nltktokenizer import NltkTokenizer
from data.repositories.pandascooccurancecounter import PandasCooccuranceCounter
from data.repositories.pandascsvreader import PandasCsvReader
from data.repositories.pypdfreader import PyPdfReader
from data.repositories.sklearnscoring import SklearnScoring
from data.repositories.urlfiledownloader import UrlFileDownloader
from data.repositories.word2vecwordembedding import Word2VecWordEmbbedding
from domain.entities.article import Article
from domain.entities.keyword import Keyword
from domain.usecases.calculatescore import CalculateScore
from domain.usecases.createcorpus import CreateCorpus
from domain.usecases.extracttext import ExtractText
from domain.usecases.hierarchicalrelationshipstrength import HierarchicalRelationshipStrength
from domain.usecases.inferpairedkeywordrelationship import InferPairedKeywordRelationship
from domain.usecases.klink import Klink
from domain.usecases.markkeywordoncorpus import MarkKeywordOnCorpus
from domain.usecases.processcooccurance import ProcessCooccurance
from domain.usecases.senttokenize import SentTokenize


def main():

    create_corpus = CreateCorpus(
        csv_reader=PandasCsvReader(), file_downloader=UrlFileDownloader(), pdf_reader=PyPdfReader())
    corpus = create_corpus.execute("corpus.csv")

    keywords = [Keyword(["experiment"]), Keyword(["experimental_software"])]

    extract_text = ExtractText(NltkSentTokenizer(), NltkTokenizer())
    tokenized_corpus = extract_text.execute(corpus)

    mark_keyword_on_corpus = MarkKeywordOnCorpus(keywords)
    mark_keyword_on_corpus.execute(tokenized_corpus)

    word2vec = Word2VecWordEmbbedding(
        tokenized_corpus.getTokenizedSentences())

    cooccurance_counter = PandasCooccuranceCounter()

    klink = Klink(word_embedding=word2vec,
                  cooccurance_counter=cooccurance_counter, year=2019)
    graph = klink.execute(keywords, tokenized_corpus)
    for merged_keyword in graph.keywords:
        print(str(merged_keyword))

    calculate_score = CalculateScore(
        graph=graph, scoring=SklearnScoring(), csv_reader=PandasCsvReader())
    calculate_score.execute("validation.csv")


if __name__ == "__main__":
    main()
