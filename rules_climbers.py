from data_validator import DataValidator
from pathlib import Path

def validate_sales_data():
    validator = DataValidator()
    
    # Add sales-specific rules
    validator.add_rule(
        name="positive_revenue",
        check_func=lambda df: (df['revenue'] >= 0).all(),
        message="Revenue contains negative values",
        severity="error"
    )
    
    validator.add_rule(
        name="valid_customer_ids",
        check_func=lambda df: df['customer_id'].notna().all(),
        message="Missing customer IDs",
        severity="error"
    )
    
    return validator.validate_file(Path('data/climbers_table.csv'))


