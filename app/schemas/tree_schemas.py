from pydantic import BaseModel, Field


class NewTreeSchema(BaseModel):
    title: str = Field(max_length=16)
    description: str | None
