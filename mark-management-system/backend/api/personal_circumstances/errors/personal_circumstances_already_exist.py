class PersonalCircumstanceAlreadyExists(Exception):
    """
    A custom subclass exception, raised when trying to create a personal circumstance which already exists.

    Args:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
