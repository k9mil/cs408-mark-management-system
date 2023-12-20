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
