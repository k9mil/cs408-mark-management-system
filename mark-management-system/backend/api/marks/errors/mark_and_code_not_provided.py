class MarkAndCodeNotProvided(Exception):
    """
    A custom subclass exception, raised when both a mark and a code were not provided

    Args:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
