from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import CharityDonation


class Donation(CharityDonation):
    comment = Column(String)
    user_id = Column(
        Integer,
        ForeignKey(
            'user.id',
            name='fk_donation_user_id_user'
        )
    )
