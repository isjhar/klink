from data.repositories.nltksenttokenizer import NltkSentTokenizer
from data.repositories.nltkstemmer import NltkStemmer
from data.repositories.nltktokenizer import NltkTokenizer
from domain.usecases.extracttext import ExtractText



def main():
    extractText = ExtractText(stemmer=NltkStemmer(), tokenizer=NltkTokenizer(), sent_tokenizer=NltkSentTokenizer())

    tokens = extractText.execute("hello im isjhar from makassar. i work as software developer.")
    print(tokens)

if __name__ == "__main__":
    main()