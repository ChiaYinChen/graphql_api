

class APIException(Exception):

    def __init__(self, message, status=None):
        self.status = status
        super().__init__(message)
