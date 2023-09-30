import argparse
from data.repositories.nltksenttokenizer import NltkSentTokenizer
from data.repositories.nltktokenizer import NltkTokenizer
from data.repositories.pandascooccurancecounter import PandasCooccuranceCounter
from data.repositories.pandascsvreader import PandasCsvReader
from data.repositories.pypdfreader import PyPdfReader
from data.repositories.sklearnscoring import SklearnScoring
from data.repositories.urlfiledownloader import UrlFileDownloader
from data.repositories.word2vecwordembedding import Word2VecWordEmbbedding
from domain.usecases.calculatescore import CalculateScore
from domain.usecases.createcorpus import CreateCorpus
from domain.usecases.createkeywords import CreateKeywords
from domain.usecases.extracttext import ExtractText
from domain.usecases.klink import Klink
from domain.usecases.markkeywordoncorpus import MarkKeywordOnCorpus


def main():
    parser = argparse.ArgumentParser(
        prog='Klink',
        description='generate relation of keywords using corpus',
        epilog='Text at the bottom of help')
    parser.add_argument('-k', '--keywords',
                        help='csv file contains list of keywords')
    parser.add_argument(
        '-c', '--corpus', help='csv file containsn list of pdf urls')
    parser.add_argument(
        '-v', '--validation', help='csv file contains validation')

    args = parser.parse_args()

    csv_reader = PandasCsvReader()

    create_corpus = CreateCorpus(
        csv_reader=csv_reader, file_downloader=UrlFileDownloader(), pdf_reader=PyPdfReader())
    corpus = create_corpus.execute(args.corpus)

    create_keywords = CreateKeywords(csv_reader)
    keywords = create_keywords.execute(args.keywords)

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
    calculate_score.execute(args.validation)


if __name__ == "__main__":
    main()
