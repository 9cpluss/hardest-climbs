from dataclasses import dataclass
from typing import Any, Callable, List, Optional
from pathlib import Path
import pandas as pd

@dataclass
class Rule:
    name: str
    check: Callable[[pd.DataFrame], bool]
    message: str
    severity: str = "error"  # error, warning, info
from dataclasses import dataclass
from typing import Any, Callable, List, Optional
from pathlib import Path
import pandas as pd

@dataclass
class Rule:
    name: str
    check: Callable[[pd.DataFrame], bool]
    message: str
    severity: str = "error"

class DataValidator:
    def __init__(self):
        self.rules: List[Rule] = []
    
    def add_rule(self, name: str, check_func: Callable, message: str, severity: str = "error"):
        """Add a new validation rule"""
        self.rules.append(Rule(name, check_func, message, severity))
    
    def validate_file(self, file_path: Path) -> List[dict]:
        """Run all rules on a given file"""
        df = pd.read_csv(file_path)  # Adjust reader based on file type
        violations = []
        
        for rule in self.rules:
            try:
                if not rule.check(df):
                    violations.append({
                        "file": str(file_path),
                        "rule": rule.name,
                        "message": rule.message,
                        "severity": rule.severity
                    })
            except Exception as e:
                violations.append({
                    "file": str(file_path),
                    "rule": rule.name,
                    "message": f"Rule execution failed: {str(e)}",
                    "severity": "error"
                })
                
        return violations

def print_validation_results(results):
    """Helper function to print validation results"""
    if not results:
        print("✅ All validations passed!")
        return
        
    print("\n🔍 Validation Results:")
    for violation in results:
        severity_symbol = "❌" if violation["severity"] == "error" else "⚠️"
        print(f"\n{severity_symbol} {violation['rule']}:")
        print(f"   Message: {violation['message']}")
        print(f"   Severity: {violation['severity']}")
        print(f"   File: {violation['file']}")