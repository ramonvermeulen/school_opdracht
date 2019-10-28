from management.request_handler import AbstractRequestHandler
from jinja2 import Environment, PackageLoader
from utils.bytes_formatter import size_formatter


class GetHandler(AbstractRequestHandler):

    def __init__(self):
        super().__init__()
        self.recent_updated_records = None
        self.all_records = None
        try:
            self.env = Environment(loader=PackageLoader('management', 'views'))
            self.template = self.env.get_template('dashboard.html')
        except Exception as e:
            print(e)

    @staticmethod
    def _process_records(records):
        generated_records = []
        for record in records:
            for key, value in record.items():
                if 'MEM' in key.upper() and not 'PERC' in key.upper() or 'SWAP' in key.upper() and not 'PERC' in key.upper():
                    record[key] = size_formatter(value)
            generated_records.append(record)
        return generated_records

    def handle_request(self, data=None):
        self.recent_updated_records = self._process_records(self.dal.get_all_recent_updated_records())
        self.all_records = self._process_records(self.dal.get_all_records())

        print(self.template.render(all_records=self.all_records, online_records=self.recent_updated_records))
