from datetime import datetime

from sqlalchemy import not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investing(
    session: AsyncSession
):
    charityproject = await session.execute(
        select(CharityProject).where(
            not_(CharityProject.fully_invested)
        )
    )
    donation = await session.execute(
        select(Donation).where(
            not_(Donation.fully_invested)
        )
    )
    charityproject = charityproject.scalars().first()
    donation = donation.scalars().first()
    if not charityproject or not donation:
        return
    charityproject_invested_left = (
        charityproject.full_amount - charityproject.invested_amount
    )
    donation_invested_left = (
        donation.full_amount - donation.invested_amount
    )

    if charityproject_invested_left <= donation_invested_left:
        donation.invested_amount += charityproject_invested_left
        charityproject.invested_amount = charityproject.full_amount
        charityproject.fully_invested = True
        charityproject.close_date = datetime.now()
    else:
        charityproject.invested_amount += donation_invested_left
        donation.invested_amount = donation.full_amount
        donation.fully_invested = True
        donation.close_date = datetime.now()
    await session.commit()
    await session.refresh(charityproject)
    await session.refresh(donation)
    await investing(session)
