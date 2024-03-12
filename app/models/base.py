from datetime import datetime

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


CHARITY_DONATION_REPRESENTATION = (
    'Сумма: {full_amount}\n'
    'Дата создания: {create_date}\n'
    'Cтатус: {fully_invested}\n'
    'Дата закрытия: {close_date}\n'
)


class CharityDonation(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('full_amount >= invested_amount'),
        CheckConstraint('invested_amount >= 0')
    )
    full_amount: Mapped[int]
    invested_amount: Mapped[int] = mapped_column(default=0)
    fully_invested: Mapped[bool] = mapped_column(default=False)
    create_date: Mapped[datetime] = mapped_column(default=datetime.now)
    close_date: Mapped[datetime] = mapped_column(nullable=True)

    def __repr__(self):
        close_date = self.close_date if self.close_date else '-'
        return CHARITY_DONATION_REPRESENTATION.format(
            full_amount=self.full_amount,
            create_date=self.create_date,
            fully_invested=self.fully_invested,
            close_date=close_date
        )
