class Keyword:
    def __init__(self, items: list):
        self.items = items
    
    def add_equal_keyword(self, new_item: str):
        inserted_index = len(self.items)-1
        for i, item in enumerate(self.items):
            if new_item < item:
                inserted_index = i
                break
        self.items.insert(inserted_index, new_item)    
        
    def __str__(self) -> str:
        return "/".join(self.items)