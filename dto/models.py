from pydantic import BaseModel


class Hello(BaseModel):
    id: str
    content: str
