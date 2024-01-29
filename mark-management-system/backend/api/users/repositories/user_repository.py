from typing import List

from api.system.models.models import User, Role


class UserRepository:
    def __init__(self, db):
        self.db = db

    def add(self, user: User) -> None:
        self.db.add(user)
        self.db.commit()
        
        self.db.refresh(user)

    def find_by_id(self, user_id: str) -> User:
        return self.db.query(User).filter_by(id=user_id).first()

    def find_by_email(self, email_address: str) -> User:
        return self.db.query(User).filter_by(email_address=email_address).first()
    
    def get_users(self, skip: int, limit: int) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_lecturers(self, skip: int, limit: int) -> List[User]:
        return self.db.query(User).join(Role, User.user_id == Role.user_id).filter(Role.role_id == 2).offset(skip).limit(limit).all()

    # TODO: remove, duplicate of find_by_id()
    def get_user(self, user_id: int) -> User:
        return self.db.query(User).filter_by(id=user_id).first()
