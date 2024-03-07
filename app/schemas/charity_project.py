from typing import Optional

from pydantic import ConfigDict, Field

from app.schemas.base import CharityProjectDonationBase
from app.schemas.schemas_examples import PROJECT_SCHEMA_EXAMPLE


class CharityProjectBase(CharityProjectDonationBase):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(max_length=100)
    description: str = Field()
    full_amount: int = Field(gt=0)
    model_config = ConfigDict(json_schema_extra=PROJECT_SCHEMA_EXAMPLE)  # type: ignore


class CharityProjectUpdate(CharityProjectBase):
    model_config = ConfigDict(json_schema_extra=PROJECT_SCHEMA_EXAMPLE)  # type: ignore


class CharityProjectDB(CharityProjectCreate):
    id: int
