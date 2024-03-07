from datetime import datetime

from app.models.base import CharityDonation


def investing(
    target: CharityDonation,
    source: CharityDonation
):
    investing_amount = min(
        (target.full_amount - target.invested_amount),
        (source.full_amount - source.invested_amount)
    )  # type: ignore
    for object in (target, source):
        object.invested_amount += investing_amount
        if object.invested_amount == object.full_amount:
            object.invested_amount = object.full_amount
            object.fully_invested = True
            object.close_date = datetime.now()
    return source
