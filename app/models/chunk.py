from typing import Dict, Any
from attr import dataclass


@dataclass(slots=True)
class ChunkData:
    id: str
    content: str
    metadata: Dict[str, Any]
    