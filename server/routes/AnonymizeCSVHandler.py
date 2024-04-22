import hashlib
import json
import numpy as np
import pandas as pd
import spacy

from enum import Enum
from flask import jsonify, request
from flask_restful import Resource

# Enum for data types
class DataType(Enum):
    DATE = 'date'
    NUMBER = 'number'
    STRING = 'string'
    
# Enum for sensitivity types
class SensitivityType(Enum):
    IDENTIFIER = 'identifier'
    INSENSITIVE = 'insensitive'
    QUASI_IDENTIFIER = 'quasi-identifier'
    SENSITIVE = 'sensitive'

class ColumnMetadata:
    def __init__(self, name: str, dataType: DataType, sensitivityType: SensitivityType) -> None:
        self.name = name
        self.dataType = DataType(dataType)
        self.sensitivityType = SensitivityType(sensitivityType)
        
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'dataType': self.dataType,
            'sensitivityType': self.sensitivityType
        }
        
    def __str__(self) -> str:
        return f"ColumnMetadata(name={self.name}, dataType={self.dataType}, sensitivityType={self.sensitivityType})"

class AnonymizeCSVHandler(Resource):
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_trf")
        
    def generalize_string(self, x: str) -> str:
        # Tokenize the string
        tokens = self.nlp(x)
        
        # Generalize the string by replacing entities with their labels
        return ' '.join([token.ent_type_ if token.ent_type_ else token.text for token in tokens])
        
    def anonymize_date(self, df: pd.DataFrame, column: ColumnMetadata) -> pd.DataFrame:
        match column.sensitivityType:
            case SensitivityType.IDENTIFIER:
                # Anonymize the identifier by hashing the date
                df[column.name] = df[column.name].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())
            case SensitivityType.INSENSITIVE:
                # Do nothing for non-sensitive columns
                pass
            case SensitivityType.QUASI_IDENTIFIER:
                # Anonymize the quasi-identifier by generalizing the date
                df[column.name] = df[column.name].apply(lambda x: x.replace(day = 1))
            case SensitivityType.SENSITIVE:
                # Anonymize the date by randomizing the date within the time period
                min_date = df[column.name].min()
                max_date = df[column.name].max()
                df[column.name] = df[column.name].apply(lambda x: min_date + pd.Timedelta(days = np.random.randint(0, (max_date - min_date).days)))
        
        return df
    
    def anonymize_number(self, df: pd.DataFrame, column: ColumnMetadata) -> pd.DataFrame:
        match column.sensitivityType:
            case SensitivityType.IDENTIFIER:
                # Anonymize the identifier by hashing the number
                df[column.name] = df[column.name].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())
            case SensitivityType.INSENSITIVE:
                # Do nothing for non-sensitive columns
                pass
            case SensitivityType.QUASI_IDENTIFIER:
                # Anonymize the quasi-identifier by binning the number
                df[column.name] = pd.cut(df[column.name], bins = 5).astype(str)
            case SensitivityType.SENSITIVE:
                # Anonymize the sensitive data by adding noise
                df[column.name] = df[column.name] + np.random.normal(0, 1, len(df))
        
        return df
    
    def anonymize_string(self, df: pd.DataFrame, column: ColumnMetadata) -> pd.DataFrame:
        match column.sensitivityType:
            case SensitivityType.IDENTIFIER:
                # Anonymize the identifier by hashing the string
                df[column.name] = df[column.name].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
            case SensitivityType.INSENSITIVE:
                # Do nothing for non-sensitive columns
                pass
            case SensitivityType.QUASI_IDENTIFIER:
                # Anonymize the quasi-identifier by generalizing using hierarchy
                df[column.name] = df[column.name].apply(self.generalize_string)
            case SensitivityType.SENSITIVE:
                # Anonymize the sensitive data by masking all characters except the first character
                df[column.name] = df[column.name].apply(lambda x: x[0] + '*' * (len(x) - 1) if len(x) > 1 else x)
        
        return df
    
    def anonymize(self, df: pd.DataFrame, column_metadata: list[ColumnMetadata]) -> pd.DataFrame:
        # Iterate over each column metadata
        for column in column_metadata:
            # Check if the column name exists in the DataFrame
            if column.name not in df.columns:
                raise Exception(f"Column '{column.name}' not found in the CSV file")
            
            # Anonymize the column based on the data type
            match column.dataType:
                case DataType.DATE:
                    df = self.anonymize_date(df, column)
                case DataType.NUMBER:
                    df = self.anonymize_number(df, column)
                case DataType.STRING:
                    df = self.anonymize_string(df, column)
                    
        return df
    
    def post(self):
        try:
            # Parse request to get the CSV file and column metadata
            file = request.files.get("file")
            column_metadata: list[ColumnMetadata] = [ColumnMetadata(**column) for column in json.loads(request.form.get("column_metadata", "[]"))]
            
            # Check if the file exists and is a CSV file
            if file is None or file.filename.split('.')[-1] != 'csv':
                raise Exception("Please provide a CSV file")
            
            # Check if the file exists and is a CSV file
            if file is None or file.filename.split('.')[-1] != 'csv':
                raise Exception("Please provide a CSV file")

            # Check if the column metadata is empty
            if not column_metadata:
                raise Exception("Please provide column metadata")
            
            # Get the column names with date type
            date_columns = [column.name for column in column_metadata if column.dataType == DataType.DATE]
            
            # Read the CSV file
            df = pd.read_csv(file, parse_dates = date_columns)
            
            # Drop all Unnamed columns
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            
            # Anonymize the data
            result = self.anonymize(df, column_metadata)
            
            # Return the anonymized data
            return jsonify(result.to_dict(orient = 'records'))
        except Exception as ex:
            return {'error': str(ex)}