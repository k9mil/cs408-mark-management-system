class ClassNotFound(Exception):
    """
    A custom subclass exception, raised when a class is not found.

    Args:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
