from typing import Any

from attr import dataclass


@dataclass(slots=True)
class DocumentData:
    content: str
    metadata: dict[str, Any]
