from attr import dataclass


@dataclass(slots=True)
class Citation:
    source: str
    page: int
