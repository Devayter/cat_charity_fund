from sqlalchemy import Column, String, Text

from app.models.base import CharityDonation


class CharityProject(CharityDonation):
    name = Column(String)
    description = Column(Text)
