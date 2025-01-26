import pandera as pa
import pandas as pd
from datetime import datetime
from pathlib import Path


# rules
def sends_schema():
    return pa.DataFrameSchema({
        'date': pa.Column(pa.DateTime, 
            pa.Check(lambda x: pd.isna(x) | (pd.to_datetime(x)<= datetime.now())), 
            nullable=True)
    })

# run rules
def validate_sends_data(file_path):
    schema = sends_schema()
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    try:
        schema.validate(df, lazy=True)
        print("Data validation successful!")
    except pa.errors.SchemaErrors as err:
        print("Data validation failed:")
        print(err.failure_cases)
validate_sends_data(Path('data/sends_table.csv'))

