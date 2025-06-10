import csv
from typing import List, Dict
class PreProcessing:
    
    def load_csv(csv_file: str, delimitador: str = ',') -> tuple:
        headers = []
        datas = []
        
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=delimitador)
            headers = next(reader)
            
            for row in reader:
                if len(row) == len(headers):
                    row_dict = {}
                    for i, column in enumerate(headers):
                        row_dict[column] = row[i]
                    datas.append(row_dict)
        return headers, datas
    
    def search_categorical_columns(datas: List[Dict], headers: List[str]) -> List[str]:
        categorical_columns = []
        
        for column in datas:
            for line in datas:
                value = line[column]
                try:
                    float(value)
                except (ValueError, TypeError):
                    if column not in categorical_columns:
                        categorical_columns.append(column)
                        break
        return categorical_columns
    
    def search_unique_values(datas: List[Dict], column: str) -> List[str]:
        unique_values = set()
        
        for line in datas:
            unique_values.add(line[column])
        return unique_values
    
    def apply_one_hot_encoding(datas: List[Dict], categorical_columns: List[str]) -> List[Dict]:
        for column in categorical_columns:
            unique_values = PreProcessing.search_unique_values(datas, column)

            for line in datas:
                value = line[column]
                for unique_value in unique_values:
                    new_column = f"{column}_{unique_value}"
                    line[new_column] = 1 if value == unique_value else 0
                del line[column]
        return datas