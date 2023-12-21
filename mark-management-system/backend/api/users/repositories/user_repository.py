from api.system.models.models import User

from api.utils.singleton import singleton


@singleton
class UserRepository:
    def __init__(self, db):
        self.db = db

    def add(self, user: User) -> None:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

    def find_by_email(self, email_address: str) -> User:
        return self.db.query(User).filter_by(email_address=email_address).first()
    
    def get_users(self, skip: int, limit: int) -> list[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_user(self, user_id: int) -> User:
        return self.db.query(User).filter_by(id=user_id).first()
