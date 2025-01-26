import pandera as pa
import pandas as pd
from datetime import datetime


current_year = datetime.now().year


climbers_schema = pa.DataFrameSchema(
    {
        'climber_id': pa.Column(
            dtype=str,
            checks=pa.Check(lambda s: not s.duplicated().any()),
            unique=True
        ),
        'gender': pa.Column(str, pa.Check.isin(['male', 'female'])),
        'year_of_birth':  pa.Column(
            dtype=float,
            checks=pa.Check(lambda x: (pd.isna(x)) | ((x >= 1970) & (x <= current_year - 15))),
            nullable=True
        )
    }
)


routes_schema = pa.DataFrameSchema(
    {
        'route_id': pa.Column(
            dtype=str,
            checks=pa.Check(lambda s: not s.duplicated().any()),
            unique=True
        ),
        'type': pa.Column(str, pa.Check.isin(['sport', 'boulder']))
    }
)


sends_schema = pa.DataFrameSchema(
    {
        'date': pa.Column(
            dtype=object,
            nullable=True
        )
    }
)


def validate_csv(file_path: str, schema: pa.DataFrameSchema):
    df = pd.read_csv(file_path)

    schema.validate(df, lazy=True)


if __name__ == "__main__":
    validate_csv(file_path='data/climbers_table.csv', schema=climbers_schema)
    validate_csv(file_path='data/routes_table.csv', schema=routes_schema)
    validate_csv(file_path='data/sends_table.csv', schema=sends_schema)
