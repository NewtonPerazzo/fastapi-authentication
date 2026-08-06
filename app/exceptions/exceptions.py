class UserNotFoundException(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.message = f"User with id '{user_id}' not found."
        super().__init__(self.message)


class UserAlreadyExistsException(Exception):
    """Exception raised when a unique user field is already registered."""

    def __init__(self, field: str):
        self.field = field
        self.message = f"A user with this {field} already exists."
        super().__init__(self.message)
