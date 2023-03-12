class DatabaseException(Exception):
    def __init__(self, message = "An error occurred when interact with database!"):
        super().__init__(message)

class EntityException(Exception):
    def __init__(self, message = "An error occurred when interact with entity!"):
        super().__init__(message)

class OperationFailed(Exception):
    def __init__(self, message = "An error occurred when implement this operation!") -> None:
        super().__init__(message)