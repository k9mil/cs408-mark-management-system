from typing import List, Optional

from sqlalchemy.orm import Session

from api.system.models.models import User
from api.system.models.models import RoleUsers

from api.system.schemas.schemas import UserEdit

from api.users.hashers.bcrypt_hasher import BCryptHasher


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, user: User) -> None:
        self.db.add(user)
        self.db.commit()
        
        self.db.refresh(user)

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter_by(id=user_id).first()

    def find_by_email(self, email_address: str) -> Optional[User]:
        return self.db.query(User).filter_by(email_address=email_address).first()
    
    def get_users(self, skip: int, limit: int) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_lecturers(self, skip: int, limit: int) -> List[User]:
        return self.db.query(User).join(RoleUsers, User.id == RoleUsers.user_id).filter(RoleUsers.role_id == 2).offset(skip).limit(limit).all()

    def update(self, user: User, request: UserEdit, hasher: BCryptHasher) -> None:
        if request.first_name and (len(request.first_name) > 1):
            user.first_name = request.first_name
  
        if request.last_name and (len(request.last_name) > 1):
            user.last_name = request.last_name

        if (request.password and request.confirm_password) and (request.password == request.confirm_password):
            user.password = hasher.hash(request.password)

        self.db.commit()
