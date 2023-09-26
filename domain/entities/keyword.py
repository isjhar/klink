class Keyword:
    def __init__(self, items: list):
        self.items = items

    def addEqualKeyword(self, new_item: str):
        inserted_index = len(self.items)-1
        for i, item in enumerate(self.items):
            if new_item < item:
                inserted_index = i
                break
        self.items.insert(inserted_index, new_item)

    def isContains(self, keyword):
        for item in keyword.items:
            if item not in self.items:
                return False
        return True

    def __str__(self) -> str:
        return "/".join(self.items)
