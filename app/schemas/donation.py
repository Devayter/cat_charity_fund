from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import CharityProjectDonationBase
from app.schemas.schemas_examples import DONATION_SCHEMA_EXAMPLE


class DonationBase(CharityProjectDonationBase):
    comment: Optional[str] = Field(..., min_length=1, max_length=200)


class DonationCreate(DonationBase):
    full_amount: int = Field(gt=0)

    model_config = ConfigDict(json_schema_extra=DONATION_SCHEMA_EXAMPLE)


class DonationDB(BaseModel):
    id: int
    comment: str
    full_amount: int
    create_date: datetime
