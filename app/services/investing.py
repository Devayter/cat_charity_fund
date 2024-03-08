from datetime import datetime

from app.models.base import CharityDonation


def investing(
    target: CharityDonation,
    sources: list[CharityDonation]
) -> list[CharityDonation]:
    investing_amount = min(
        (target.full_amount - target.invested_amount),
        sum(
            (source.full_amount - source.invested_amount) for source in sources
        )
    )  # type: ignore
    target.invested_amount += investing_amount
    for source in sources:
        source_investing_amount = min(
            (source.full_amount - source.invested_amount),
            investing_amount
        )
        source.invested_amount += source_investing_amount
        investing_amount -= source_investing_amount
    for object in (target, *sources):
        if object.invested_amount == object.full_amount:
            object.fully_invested = True
            object.close_date = datetime.now()
    return sources
