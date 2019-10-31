
class RequestStatus:
    """
    >>> r = RequestStatus()
    >>> isinstance(r, RequestStatus)
    True

    Request status class to easily return a response status and message
    """
    def __init__(self, status_code, message):
        """
        >>> r = RequestStatus(404, 'Boom! Error!')
        >>> isinstance(r, RequestStatus)
        True
        >>> r.status_code == 404:
        True
        >>> r.message == 'Boom! Error!':
        True
        """
        self.status_code = status_code
        self.message = message

    def __repr__(self):
        return f'Status:{self.status_code}\r\n\r\n{self.message}'
