from data.repositories.nltksenttokenizer import NltkSentTokenizer
from data.repositories.nltkstemmer import NltkStemmer
from data.repositories.nltktokenizer import NltkTokenizer
from data.repositories.pandascooccurancecounter import PandasCooccuranceCounter
from domain.usecases.extracttext import ExtractText
from domain.usecases.markkeywordonsentences import MarkKeywordOnSentences
from domain.usecases.namesimilarity import NameSimilarity
from domain.usecases.processcooccurance import ProcessCooccurance
from domain.usecases.senttokenize import SentTokenize



def main():
    keywords = [["im", "isjhar"], ["from"], ["i"], ["work"]]
    corpus = "hello im isjhar from makassar. i work as software developer."
    processCooccurance = ProcessCooccurance(stemmer=NltkStemmer(), tokenizer=NltkTokenizer(), sent_tokenizer=NltkSentTokenizer(), cooccurance_counter=PandasCooccuranceCounter())
    processCooccurance.execute(keywords, "hello im isjhar from makassar. i work as software developer.")    

    name_similarity = NameSimilarity(tokenizer=NltkTokenizer, stemmer=NltkStemmer())
    print(name_similarity.execute(["isjhar","test"], ["test", "gan"]))

    extract_text = ExtractText(sent_tokenizer=NltkSentTokenizer(), tokenizer=NltkTokenizer())
    tokenized_sentences = extract_text.execute(corpus)
    mark_keyword_on_sentences = MarkKeywordOnSentences()
    mark_keyword_on_sentences.execute(keywords, tokenized_sentences)


if __name__ == "__main__":
    main()