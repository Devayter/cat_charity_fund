from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import CharityDonation


DONATION_REPRESENTATION = (
    'Пользователь: {user_id}\n'
    'Комментарий: {comment}'
)


class Donation(CharityDonation):
    comment: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'user.id',
            name='fk_donation_user_id_user'
        )
    )

    def __repr__(self):
        comment = self.comment if self.comment else '-'
        return (
            super().__repr__() +
            DONATION_REPRESENTATION.format(
                user_id=self.user_id,
                comment=comment
            )
        )
