"""Util function."""


class APIException(Exception):
    """Exception for graphql API."""

    def __init__(self, message, status=None):
        """Set http status code."""
        self.status = status
        super().__init__(message)
