from dq.data_validator import DataValidator
from pathlib import Path

def validate_sends_table():
    validator = DataValidator()
    
    # No dates past today
    validator.add_rule(
    name="valid_date",
    check_func=lambda df: (
        pd.to_datetime(df['date'], errors='coerce') < datetime.now()
    ).all(),
    message="Date must be earlier than today",
    severity="error"
)
    
    return validator.validate_file(Path('data/sends_table.csv'))


