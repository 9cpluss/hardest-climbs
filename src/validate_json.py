from jsonschema import validate
import json


schema = {
    "type": "array",
    "items": {
    	"type": "object",
        "properties": {
        	"name": {"type": "string"},
            "grade": {"type": "string"},
            "fa": {"type": "string"},
            "date": {"type": "string"},
            "repeat": {"type": "array", "items": {"type": "string"}},
            "videos": {"type": "object"}
        },
        "required": ["name", "grade", "fa", "repeat", "videos"]
    }
}


with open("data/boulder.json", "r") as f:
    boulder_data = json.load(f)

with open("data/lead.json", "r") as f:
    lead_data = json.load(f)

validate(instance=boulder_data, schema=schema)
validate(instance=lead_data, schema=schema)
