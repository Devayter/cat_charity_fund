from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class CharityProjectDonationBase(BaseModel):
    full_amount: Optional[int] = Field(..., gt=0)
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime = Field(default_factory=datetime.now)
    close_date: Optional[datetime] = None
