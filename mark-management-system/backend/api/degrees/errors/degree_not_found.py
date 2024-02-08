class DegreeNotFound(Exception):
    """
    A custom subclass exception, raised when a degree is not found.

    Args:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
