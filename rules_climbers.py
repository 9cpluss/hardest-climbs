from data_validator import DataValidator
from pathlib import Path


# Get current year dynamically
current_year = datetime.now().year

def validate_climbers_table():
    validator = DataValidator()
    
    # climber_id must be unique
    validator.add_rule(
        name="Unique climber_id",
        check_func=lambda df: not df['climber_id'].duplicated().any(),
        message="Duplicated customer_id, please investigate!",
        severity="error"
    )

    # gender is M/F
    validator.add_rule(
        name="valid_gender",
        check_func=lambda df: df['gender'].isin(['male', 'female']).all(),
        message="Invalid gender values found - must be 'male' or 'female'",
        severity="error"
    )
    
    # No climbers suspiciously old or young...
    validator.add_rule(
        name="valid_birth_year",
        check_func=lambda df: (
            (df['year_of_birth'] >= 1970) & 
            (df['year_of_birth'] <= current_year - 15)
        ).all(),
        message=f"Birth year must be between 1970 and {current_year - 15} (15 years old)",
        severity="error"
    )   


    return validator.validate_file(Path('data/climbers_table.csv'))


