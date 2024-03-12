from datetime import datetime

from app.models.base import CharityDonation


def investing(
    target: CharityDonation,
    sources: list[CharityDonation]
) -> list[CharityDonation]:
    changed = []
    for source in sources:
        investing_amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        changed.append(source)
        for object in (target, source):
            object.invested_amount += investing_amount
            if object.invested_amount == object.full_amount:
                object.fully_invested = True
                object.close_date = datetime.now()
        if target.fully_invested:
            break

    return changed
