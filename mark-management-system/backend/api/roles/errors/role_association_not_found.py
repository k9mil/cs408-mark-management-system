class RoleAssociationNotFound(Exception):
    """
    A custom subclass exception, raised when a role association has not been found between a user and a role.

    Args:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
