from typing import Optional

from sqlalchemy.orm import Session

from api.system.models.models import Role
from api.system.models.models import RoleUsers
from api.system.models.models import User

from api.system.schemas.schemas import RoleUsersData

class RolesRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, role_id: int) -> Optional[Role]:
        return self.db.query(Role).filter_by(id=role_id).first()

    def find_role_association(self, request: RoleUsersData) -> Optional[RoleUsers]:
        return self.db.query(RoleUsers).filter_by(
            role_id=request.role_id,
            user_id=request.user_id
        ).first()

    def add_user(self, role_user: RoleUsers, user: User) -> None:
        self.db.add(role_user)

        self.db.commit()
        self.db.refresh(user)

    def remove_user(self, role_user: RoleUsers, user: User) -> None:
        self.db.delete(role_user)
        
        self.db.commit()
        self.db.refresh(user)
