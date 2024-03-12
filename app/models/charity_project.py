from sqlalchemy.orm import Mapped

from app.models.base import CharityDonation


CHARITYPROJECT_REPRESENTATION = (
    'Имя: {name}\n'
    'Описание: {description}\n'
)


class CharityProject(CharityDonation):
    name: Mapped[str]
    description: Mapped[str]

    def __repr__(self):
        return (
            super().__repr__() +
            CHARITYPROJECT_REPRESENTATION.format(
                name=self.name,
                description=self.description
            )
        )
