from typing import Any

from attr import dataclass


@dataclass(slots=True)
class ChunkData:
    id: str
    content: str
    metadata: dict[str, Any]
