import pandera as pa
import pandas as pd
from datetime import datetime
from pathlib import Path

current_year = datetime.now().year

# rules
def climbers_schema():
    return pa.DataFrameSchema({
        'climber_id': pa.Column(str, pa.Check(lambda s: not s.duplicated().any()), 
                                unique=True),
        'gender': pa.Column(str, pa.Check.isin(['male', 'female'])),
        'year_of_birth':  pa.Column(float, pa.Check(lambda x: (pd.isna(x)) | ((x >= 1970) & (x <= current_year - 15))), nullable=True)
    })

# run rules
def validate_climbers_data(file_path):
    schema = climbers_schema()
    df = pd.read_csv(file_path)
    try:
        schema.validate(df, lazy=True)
        print("Data validation successful!")
    except pa.errors.SchemaErrors as err:
        print("Data validation failed:")
        print(err.failure_cases)
validate_climbers_data(Path('data/climbers_table.csv'))

