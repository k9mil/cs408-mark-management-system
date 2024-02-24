class InvalidCredentials(Exception):
    """
    A custom subclass exception, raised when the provided user credentials do not match, and/or
    do not exist.

    Args:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
