from management.request_handler import AbstractRequestHandler
from utils.payload import PayLoad
from utils.status import RequestStatus


class PostHandler(AbstractRequestHandler):

    def __init__(self):
        super().__init__()

    def handle_request(self, data=None):
        try:
            payload = PayLoad(data=data)
            if self.dal.already_exists(payload.IDENTIFIER):
                self.dal.update_record(payload)
            else:
                self.dal.insert_new_record(payload)
            print(RequestStatus(200, 'Successfully added data'))
        except Exception as e:
            print(RequestStatus(500, 'Internal server errors!\nCheck the apache logs for more information.' + e))
            print(e)
