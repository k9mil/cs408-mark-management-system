class RoleNotFound(Exception):
    """
    A custom subclass exception, raised when a role has not been found.

    Args:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
