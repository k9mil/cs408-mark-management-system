class ClassesNotFound(Exception):
    """
    A custom subclass exception, raised when classes are not found.

    Attributes:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
