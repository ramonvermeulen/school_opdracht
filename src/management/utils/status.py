
class RequestStatus:
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

    def __repr__(self):
        return f'Status:{self.status_code}\r\n\r\n{self.message}'
