from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TitledTreeSchema(BaseModel):
    title: str = Field(max_length=16)


class NewTreeSchema(TitledTreeSchema):
    description: str | None


class PublicTreeSchema(TitledTreeSchema):
    id: UUID
    updated_at: datetime
