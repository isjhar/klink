from domain.repositories.cooccurancecounter import CooccuranceCounter
from domain.repositories.cooccurancematrix import CooccuranceMatrix
from domain.repositories.senttokenizer import SentTokenizer
from domain.repositories.tokenizer import Tokenizer
from domain.usecases.extracttext import ExtractText
from domain.usecases.markkeywordonsentences import MarkKeywordOnSentences


class ProcessCooccurance:
    def __init__(self, cooccurance_counter: CooccuranceCounter):        
        self.cooccurance_counter = cooccurance_counter
        
    def execute(self, keywords, marked_tokenized_sentences) -> CooccuranceMatrix:        
        return self.cooccurance_counter.process(keywords, marked_tokenized_sentences)