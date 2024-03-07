from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import CharityDonation


DONATION_REPRESENTATION = (
    'Пользователь: {user_id}\n'
    'Комментарий: {comment}'
)


class Donation(CharityDonation):
    comment = Column(String)
    user_id = Column(
        Integer,
        ForeignKey(
            'user.id',
            name='fk_donation_user_id_user'
        )
    )

    def __repr__(self):
        comment = self.comment if self.comment else '-'
        return (
            f'{super().__repr__()}'
            f'{
                DONATION_REPRESENTATION.format(
                    user_id=self.user_id,
                    comment=comment
                )
            }'
        )
