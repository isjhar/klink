class PreprocessKeyword:
    def execute(self, keyword) -> str:
        return keyword.strip().lower().replace(" ", "_")
