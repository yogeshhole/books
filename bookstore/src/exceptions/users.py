class UserAlreadyExistsException(Exception):
    def __init__(self, errors):
        message = "User already exists."
        super().__init__(message)

        self.errors = errors
