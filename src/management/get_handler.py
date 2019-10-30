import json
import urllib.error
import urllib.request
import time
import matplotlib.pyplot as plt
import base64
import numpy as np
from io import BytesIO

from jinja2 import Environment, PackageLoader

from management.request_handler import AbstractRequestHandler
from utils.bytes_formatter import size_formatter


class GetHandler(AbstractRequestHandler):

    def __init__(self):
        super().__init__()
        self.random_quote_api = 'https://api.quotable.io/random'
        self.online_machines = None
        self.offline_machines = None
        self.random_quote_content = None
        self.random_quote_author = None
        self.graph_data = None
        try:
            self.env = Environment(loader=PackageLoader('management', 'views'))
            self.template = self.env.get_template('dashboard.html')
        except Exception as e:
            print(e)

    @staticmethod
    def _prepare_data(records):
        generated_records = []
        for record in records:
            for key, value in record.items():
                if 'MEM' in key.upper() and not 'PERC' in key.upper() or 'SWAP' in key.upper() and not 'PERC' in key.upper():
                    record[key] = size_formatter(value)
                elif 'PERC' in key.upper():
                    record[key] = f'{value}%'
                elif 'LAST_UPDATED' in key.upper():
                    record[key] = time.strftime('%d-%m-%y %H:%M:%S', time.gmtime(int(value)))
            generated_records.append(record)
        return generated_records

    def _get_random_quote(self):
        try:
            response = urllib.request.urlopen(self.random_quote_api)
            encoding = response.info().get_content_charset('utf-8')
            json_response = json.loads(response.read().decode(encoding))
            self.random_quote_content = json_response.get('content')
            self.random_quote_author = json_response.get('author')
        except urllib.error.HTTPError:
            self.random_quote_content = 'An error occurred while trying to fetch from the Quote API'
            self.random_quote_author = 'System'
        except urllib.error.URLError:
            self.random_quote_content = 'The API Url is not valid'
            self.random_quote_author = 'System'
        except json.decoder.JSONDecodeError:
            self.random_quote_content = 'Something went wrong decoding the JSON response'
            self.random_quote_author = 'System'
        except Exception:
            self.random_quote_content = 'Some kind of error occurred'
            self.random_quote_author = 'System'

    def handle_request(self, data=None):
        self.offline_machines = self.dal.get_older_records()
        self.online_machines = self.dal.get_all_recent_updated_records()
        machines = ()
        data = []

        for record in self.online_machines:
            machines += (record.get('id'),)
            data.append(float(record.get('mem_used_perc')))
        y_pos = [i for i, _ in enumerate(machines)]

        plt.barh(y_pos, data)
        plt.yticks(y_pos, machines, )
        # plt.yscale(100)
        plt.xlabel('Memory used percentage')
        plt.ylabel('Machines')
        plt.tight_layout()
        plt.gca().set_xlim([0, 100])


        tmpfile = BytesIO()
        plt.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue())
        self.graph_data = encoded.decode('utf-8')

        self._get_random_quote()
        self.online_machines = self._prepare_data(self.dal.get_all_recent_updated_records())
        self.offline_machines = self._prepare_data(self.dal.get_older_records())

        print(self.template.render(
            online_machines=self.online_machines,
            offline_machines=self.offline_machines,
            random_quote_content=self.random_quote_content,
            random_quote_author=self.random_quote_author,
            graph_data=self.graph_data
        ))
