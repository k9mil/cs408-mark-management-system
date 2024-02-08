class RoleAssociationAlreadyExists(Exception):
    """
    A custom subclass exception, raised when a role association between a user & role already exists.

    Args:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
