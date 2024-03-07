from sqlalchemy import Column, String, Text

from app.models.base import CharityDonation


CHARITYPROJECT_REPRESENTATION = (
    'Имя: {name}\n'
    'Описание: {description}\n'
)


class CharityProject(CharityDonation):
    name = Column(String)
    description = Column(Text)

    def __repr__(self):
        return (
            f'{super().__repr__()}'
            f'{
                CHARITYPROJECT_REPRESENTATION.format(
                    name=self.name,
                    description=self.description
                )
            }'
        )
