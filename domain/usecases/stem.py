class Stem:
    def __init__(self, stemmer):
        self.stemmer = stemmer
    def execute(self, token):
        return self.stemmer.stem(token)