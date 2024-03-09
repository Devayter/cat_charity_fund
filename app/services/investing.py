from datetime import datetime

from app.models.base import CharityDonation


def investing(
    target: CharityDonation,
    sources: list[CharityDonation]
) -> list[CharityDonation]:
    changed_sources = []
    for source in sources:
        source_investing_amount = min(
            (source.full_amount - source.invested_amount),
            (target.full_amount - target.invested_amount)
        )  # type: ignore
        if source_investing_amount == 0:
            break
        changed_sources.append(source)
        for object in (target, source):
            object.invested_amount += source_investing_amount
            if object.invested_amount == object.full_amount:
                object.fully_invested = True
                object.close_date = datetime.now()
    return changed_sources
