class MarkNotFound(Exception):
    """
    A custom subclass exception, raised when trying to retrieve a mark which doesn't exist.

    Args:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
