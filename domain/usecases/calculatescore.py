from domain.entities.graph import Graph
from domain.entities.scoring import Scoring
from domain.repositories.csvreader import CsvReader
from domain.usecases.preprocesskeyword import PreprocessKeyword


class CalculateScore:
    def __init__(self, graph: Graph, csv_reader: CsvReader, scoring: Scoring):
        self.graph = graph
        self.csv_reader = csv_reader
        self.scoring = scoring
        self.preprocess_keyword = PreprocessKeyword()

    def execute(self, validation_file_name):
        rows = self.csv_reader.read(validation_file_name)
        validations = []
        predictions = []
        for row in rows:
            keyword1 = self.preprocess_keyword.execute(row[0])
            keyword2 = self.preprocess_keyword.execute(row[1])
            relationship = row[2].strip().lower()
            predicted_relationship = self.getPredictedRelationship(
                keyword1, keyword2)
            validations.append(relationship)
            predictions.append(predicted_relationship)

        self.scoring.score(validations, predictions)

    def getPredictedRelationship(self, keyword1: str, keyword2: str) -> str:
        for merged_keyword in self.graph.keywords:
            if keyword1 in merged_keyword.items and keyword2 in merged_keyword.items:
                return "equal"

        for predicted_keyword1 in self.graph.relationships:
            if keyword1 in predicted_keyword1.items:
                predicted_keyword2 = self.graph.relationships[predicted_keyword1]
                if keyword2 in predicted_keyword2.items:
                    return "subclassof"
        return "none"
