
import pandera as pa
import pandas as pd
from datetime import datetime
from pathlib import Path

current_year = datetime.now().year

# rules
def routes_schema():
    return pa.DataFrameSchema({
        'route_id': pa.Column(str, pa.Check(lambda s: not s.duplicated().any()), 
                                unique=True),
        'type': pa.Column(str, pa.Check.isin(['sport', 'boulder']))
    })

# run rules
def validate_routes_data(file_path):
    schema = routes_schema()
    df = pd.read_csv(file_path)
    try:
        schema.validate(df, lazy=True)
        print("Data validation successful!")
    except pa.errors.SchemaErrors as err:
        print("Data validation failed:")
        print(err.failure_cases)

validate_routes_data(Path('data/routes_table.csv'))

