class DBWriteError(Exception):
    def __init__(self, errors):
        message = "Failed to write DB record."
        super().__init__(message)

        self.errors = errors
