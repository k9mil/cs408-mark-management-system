from typing import Optional

from sqlalchemy.orm import Session

from api.system.models.models import Role
from api.system.models.models import RoleUsers
from api.system.models.models import User

from api.system.schemas.schemas import RoleUsersData

class RolesRepository:
    """The repository layer which performs queries and operations on the database for `Roles` & `RoleUsers` objects."""

    def __init__(self, db: Session) -> None:
        """
        Initializes the repository with a databance instance via Dependency Inversion.

        Args:
            db: The database session.
        """
        self.db = db

    def add(self, role: Role) -> None:
        """
        Adds an object into the database.

        Args:
            role: The object to be added.
        """
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)

    def find_by_id(self, role_id: int) -> Optional[Role]:
        """
        Retrieves a role by a given identifier.

        Args:
            role_id: The role identifier.
        
        Returns:
            Optional[Role]: A `Role` object from the database, however can also return `None` if not found.
        """
        return self.db.query(Role).filter_by(id=role_id).first()

    def find_role_association(self, request: RoleUsersData) -> Optional[RoleUsers]:
        """
        Retrieves a role association between a user & role.

        Args:
            request:  A `RoleUsersData` schematic object which contains a user_id & role_id.
        
        Returns:
            Optional[RoleUsers]: A `RoleUsers` object from the database, however can also return `None` if not found.
        """
        return self.db.query(RoleUsers).filter_by(
            role_id=request.role_id,
            user_id=request.user_id
        ).first()

    def add_user(self, role_user: RoleUsers, user: User) -> None:
        """
        Adds an association into the database.

        Args:
            role_user: A `RoleUsers` object containing the data to be inserted.
            user: A `user` object, which is not added but refreshed, to maintain consistency between states in the application.
        """
        self.db.add(role_user)

        self.db.commit()
        self.db.refresh(user)

    def remove_user(self, role_user: RoleUsers, user: User) -> None:
        """
        Removes an association from the database.

        Args:
            role_user: A `RoleUsers` object containing the data to be removed.
            user: A `user` object, which is not deleted but refreshed, to maintain consistency between states in the application.
        """
        self.db.delete(role_user)
        
        self.db.commit()
        self.db.refresh(user)
