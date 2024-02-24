class LecturersNotFound(Exception):
    """
    A custom subclass exception, raised querying for lecturers, but none are found.

    Args:
        message: A parameter which allows for a custom error message.
    """
    def __init__(self, message: str) -> None:
        self.message = message
