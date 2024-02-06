class ClassAlreadyExists(Exception):
    """
    A custom subclass exception, raised when trying to create 
    (or edit with existing class details) a class which already exists.

    Attributes:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
