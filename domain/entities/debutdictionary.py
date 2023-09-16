class DebutDictionary:
    def __init__(self) -> None:
        self.dict = {}

    def add(self, keyword, year):
        if not (keyword in self.dict) or year >= self.dict[keyword]:
            self.dict[keyword] = year
