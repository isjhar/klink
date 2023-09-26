from domain.repositories.csvreader import CsvReader
import pandas as pd


class PandasCsvReader(CsvReader):
    def __init__(self) -> None:
        pass

    def read(self, file_name) -> list:
        df = pd.read_csv(file_name)
        return df.values.tolist()
