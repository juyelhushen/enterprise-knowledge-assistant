from pydantic import BaseModel


class Citation(BaseModel):
    source: str
    page: int
