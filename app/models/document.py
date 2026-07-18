from typing import Dict, Any

from attr import dataclass


@dataclass(slots=True)
class DocumentData:
    content: str
    metadata: Dict[str, Any]