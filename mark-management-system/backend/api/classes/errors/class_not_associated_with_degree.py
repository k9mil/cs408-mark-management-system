class ClassNotAssociatedWithDegree(Exception):
    """
    A custom subclass exception, raised when a given class code does not belong to a given degree.

    Args:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
