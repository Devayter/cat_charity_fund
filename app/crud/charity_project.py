from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    pass


charityproject_crud = CRUDCharityProject(CharityProject)
