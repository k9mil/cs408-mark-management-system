from api.system.models.models import Role
from api.system.models.models import RoleUsers

from api.system.schemas.schemas import RoleUsersData

from api.utils.singleton import singleton


@singleton
class RolesRepository:
    def __init__(self, db):
        self.db = db

    def find_by_id(self, role_id: int) -> Role:
        return self.db.query(Role).filter_by(id=role_id).first()

    def find_role_association(self, request: RoleUsersData) -> RoleUsers:
        return self.db.query(RoleUsers).filter_by(
            role_id=request.role_id,
            user_id=request.user_id
        ).first()

    def add_user(self, role_user: RoleUsers) -> None:
        self.db.add(role_user)
        self.db.commit()

    def remove_user(self, role_user: RoleUsers) -> None:
        self.db.delete(role_user)
        self.db.commit()
