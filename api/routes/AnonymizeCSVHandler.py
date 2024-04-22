import hashlib
import json
import numpy as np
import pandas as pd
import spacy

from enum import Enum
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from typing import Annotated

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

nlp = spacy.load("en_core_web_trf")
        
def generalize_string(x: str) -> str:
    # Tokenize the string
    tokens = nlp(x)
    
    # Generalize the string by replacing entities with their labels
    return ' '.join([token.ent_type_ if token.ent_type_ else token.text for token in tokens])
    
def anonymize_date(df: pd.DataFrame, column: ColumnMetadata) -> pd.DataFrame:
    if column.sensitivityType == SensitivityType.IDENTIFIER:
        df[column.name] = df[column.name].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())
    elif column.sensitivityType == SensitivityType.INSENSITIVE:
        pass # Do nothing for non-sensitive columns
    elif column.sensitivityType == SensitivityType.QUASI_IDENTIFIER:
        df[column.name] = df[column.name].apply(lambda x: x.replace(day = 1))
    elif column.sensitivityType == SensitivityType.SENSITIVE:
        min_date = df[column.name].min()
        max_date = df[column.name].max()
        df[column.name] = df[column.name].apply(lambda x: min_date + pd.Timedelta(days = np.random.randint(0, (max_date - min_date).days)))
    else:
        raise Exception(f"Invalid sensitivity type '{column.sensitivityType}' for date column '{column.name}'")
    
    return df

def anonymize_number(df: pd.DataFrame, column: ColumnMetadata) -> pd.DataFrame:
    if column.sensitivityType == SensitivityType.IDENTIFIER:
        df[column.name] = df[column.name].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())
    elif column.sensitivityType == SensitivityType.INSENSITIVE:
        pass # Do nothing for non-sensitive columns
    elif column.sensitivityType == SensitivityType.QUASI_IDENTIFIER:
        df[column.name] = pd.cut(df[column.name], bins = 5).astype(str)
    elif column.sensitivityType == SensitivityType.SENSITIVE:
        df[column.name] = df[column.name] + np.random.normal(0, 1, len(df))
    else:
        raise Exception(f"Invalid sensitivity type '{column.sensitivityType}' for number column '{column.name}'")
    
    return df

def anonymize_string(df: pd.DataFrame, column: ColumnMetadata) -> pd.DataFrame:
    if column.sensitivityType == SensitivityType.IDENTIFIER:
        df[column.name] = df[column.name].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
    elif column.sensitivityType == SensitivityType.INSENSITIVE:
        pass # Do nothing for non-sensitive columns
    elif column.sensitivityType == SensitivityType.QUASI_IDENTIFIER:
        df[column.name] = df[column.name].apply(generalize_string)
    elif column.sensitivityType == SensitivityType.SENSITIVE:
        df[column.name] = df[column.name].apply(lambda x: x[0] + '*' * (len(x) - 1) if len(x) > 1 else x)
    else:
        raise Exception(f"Invalid sensitivity type '{column.sensitivityType}' for string column '{column.name}'")
    
    return df

def anonymize(df: pd.DataFrame, column_metadata: list[ColumnMetadata]) -> pd.DataFrame:
    # Iterate over each column metadata
    for column in column_metadata:
        # Check if the column name exists in the DataFrame
        if column.name not in df.columns:
            raise Exception(f"Column '{column.name}' not found in the CSV file")
        
        # Anonymize the column based on the data type
        if column.dataType == DataType.DATE:
            df = anonymize_date(df, column)
        elif column.dataType == DataType.NUMBER:
            df = anonymize_number(df, column)
        elif column.dataType == DataType.STRING:
            df = anonymize_string(df, column)
        else:
            raise Exception(f"Invalid data type '{column.dataType}' for column '{column.name}'")
                
    return df

router = APIRouter()

@router.post("/")
async def anonymize_csv(
    file: Annotated[UploadFile, File(...)],
    column_metadata: Annotated[str, Form()]
) -> dict:
    try:
        if not file.filename.endswith('.csv'):
            raise Exception("Invalid file format. Please upload a CSV file")
        if not column_metadata:
            raise Exception("Column metadata is required for anonymization")
        
        column_metadata = [ColumnMetadata(**column) for column in json.loads(column_metadata)]
        df = pd.read_csv(file.file, parse_dates=[column.name for column in column_metadata if column.dataType == DataType.DATE])
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        result = anonymize(df, column_metadata)
        
        return {
            "status_code": 200,
            "data": result.to_dict(orient = 'records')
        }
    except Exception as ex:
        return HTTPException(status_code=500, detail=str(ex))