class UserNotFoundException(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, user: str):
        self.user_id = user
        self.message = f"User with '{user}' not found."
        super().__init__(self.message)

class SessionNotFoundException(Exception):
    """Exception raised when a session is not found."""

    def __init__(self):
        self.message = f"Session not found."
        super().__init__(self.message)

class ResetPasswordException(Exception):
    """Exception raised when a reset password get fail."""

    def __init__(self):
        self.message = f"Reset password get fail"
        super().__init__(self.message)

class CantCreateSessionException(Exception):
    """Exception raised when a session is not created."""

    def __init__(self):
        self.message = f"Can't create a session."
        super().__init__(self.message)

class CantUpdateSessionException(Exception):
    """Exception raised when a session is not updated."""

    def __init__(self):
        self.message = f"Can't update a session."
        super().__init__(self.message)

class CantRevokeSessionException(Exception):
    """Exception raised when a session is not revoked."""

    def __init__(self):
        self.message = f"Can't revoked a session."
        super().__init__(self.message)


class UserAlreadyExistsException(Exception):
    """Exception raised when a unique user field is already registered."""

    def __init__(self, field: str):
        self.field = field
        self.message = f"A user with this {field} already exists."
        super().__init__(self.message)

class InvalidCredentialsException(Exception):
    def __init__(self):
        super().__init__("Invalid email or password.")

class InactiveUserException(Exception):
    def __init__(self):
        super().__init__("User account is inactive.")


class InvalidAccessTokenException(Exception):
    def __init__(self):
        super().__init__("Invalid access token.")


class AccessTokenExpiredException(Exception):
    def __init__(self):
        super().__init__("Access token has expired.")


class InvalidRefreshTokenException(Exception):
    def __init__(self):
        super().__init__("Invalid refresh token.")


class RefreshTokenExpiredException(Exception):
    def __init__(self):
        super().__init__("Refresh token has expired.")


class SessionRevokedException(Exception):
    def __init__(self):
        super().__init__("Session has been revoked.")
