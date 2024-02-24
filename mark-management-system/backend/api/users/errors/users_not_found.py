class UsersNotFound(Exception):
    """
    A custom subclass exception, raised when querying for users, nothing is
    returned.

    Args:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
