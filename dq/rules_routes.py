from dq.data_validator import DataValidator
from pathlib import Path

def validate_routes_table():
    validator = DataValidator()
    
    
    # route_id must be unique
    validator.add_rule(
        name="Unique route_id",
        check_func=lambda df: not df['route_id'].duplicated().any(),
        message="Duplicated route_id, please investigate!",
        severity="error"
    )

     # route_name must be unique
    validator.add_rule(
        name="Unique route_name",
        check_func=lambda df: not df['route_name'].duplicated().any(),
        message="Duplicated route_name, please investigate!",
        severity="error"
    )


    # type is sport or boulder
    validator.add_rule(
        name="type",
        check_func=lambda df: df['type'].isin(['sport', 'boulder']).all(),
        message="Invalid type values found - must be 'sport' or 'boulder'",
        severity="error"
    )
    
    return validator.validate_file(Path('data/routes_table.csv'))


