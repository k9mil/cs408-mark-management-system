from typing import List, Optional

from sqlalchemy.orm import Session

from api.system.models.models import User
from api.system.models.models import RoleUsers

from api.system.schemas.schemas import UserEdit

from api.users.hashers.bcrypt_hasher import BCryptHasher


class UserRepository:
    """The repository layer which performs queries and operations on the database for `User` objects."""

    def __init__(self, db: Session):
        """
        Initializes the repository with a databance instance via Dependency Inversion.

        Args:
            db: The database session.
        """
        self.db = db

    def add(self, user: User) -> None:
        """
        Adds an object into the database.

        Args:
            user: The object to be added.
        """
        self.db.add(user)
        self.db.commit()
        
        self.db.refresh(user)

    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieves a user by a given user_id identifier.

        Args:
            user_id: The user identifier.
        
        Returns:
            Optional[User]: A `User` from the database, however can also return `None` if not found.
        """
        return self.db.query(User).filter_by(id=user_id).first()

    def find_by_email(self, email_address: str) -> Optional[User]:
        """
        Retrieves a user by a given email_address identifier.

        Args:
            email_address: The user's email_address, the identifier..
        
        Returns:
            Optional[User]: A `User` from the database, however can also return `None` if not found.
        """
        return self.db.query(User).filter_by(email_address=email_address).first()
    
    def get_users(self, skip: int, limit: int) -> List[User]:
        """
        Retrieves a list of users in the system, given a skip and a limit.

        Args:
            skip: The amount to skip.
            limit: The maximum number of items to be retrieved.
        
        Returns:
            List[User]: A list of `User` schematic objects, however can also return an empty list if nothing is found.
        """
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_lecturers(self, skip: int, limit: int) -> List[User]:
        """
        Retrieves a list of users with the `Lecturer` role in the system, given a skip and a limit.

        Args:
            skip: The amount to skip.
            limit: The maximum number of items to be retrieved.
        
        Returns:
            List[User]: A list of `User` schematic objects, however can also return an empty list if nothing is found.
        """
        return self.db.query(User).join(RoleUsers, User.id == RoleUsers.user_id).filter(RoleUsers.role_id == 2).offset(skip).limit(limit).all()

    def update(self, user: User, request: UserEdit, hasher: BCryptHasher) -> None:
        """
        Updates the details of an existing user.

        Args:
            user: A user object, which already exists in the database.
            request: An object that conforms with the `UserEdit` schema, containing the new information of the user.
            hasher: An instance of a hasher, used to hash the password if a password is present in the request.
        """
        if request.first_name and (len(request.first_name) > 1):
            user.first_name = request.first_name
  
        if request.last_name and (len(request.last_name) > 1):
            user.last_name = request.last_name

        if (request.password and request.confirm_password) and (request.password == request.confirm_password):
            user.password = hasher.hash(request.password)

        self.db.commit()
