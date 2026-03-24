import json
from typing import Dict, Any

def render_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, indent=2, default=str)