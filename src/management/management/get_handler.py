import json
import urllib.error
import urllib.request
import time
import matplotlib.pyplot as plt
import base64
from io import BytesIO

from jinja2 import Environment, PackageLoader

from management.request_handler import AbstractRequestHandler
from utils import size_formatter


class GetHandler(AbstractRequestHandler):

    def __init__(self):
        super().__init__()
        self.random_quote_api = 'https://api.quotable.io/random'
        self.online_machines = None
        self.offline_machines = None
        self.random_quote_content = None
        self.random_quote_author = None
        self.graph_data_mem = None
        self.graph_data_cpu = None
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
            encoding = response.info().get_content_charset('ascii')
            json_response = json.loads(response.read().decode(encoding))
            self.random_quote_content = json_response.get('content')
            self.random_quote_author = json_response.get('author')
        except UnicodeDecodeError:
            self.random_quote_content = 'Couldn\'t decode the data from the Quote API to ascii'
            self.random_quote_author = 'System'
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

    def _generate_graph_base64_string(self, data_key, x_label, y_label, minimum=0, maximum=100):
        machines = ()
        data = []

        for record in self.online_machines:
            machines += (record.get('id'),)
            data.append(float(record.get(data_key)))
        y_pos = [i for i, _ in enumerate(machines)]

        plt.rcParams['figure.figsize'] = (25, 10)

        plt.barh(y_pos, data)
        plt.yticks(y_pos, machines, )
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.tight_layout()
        plt.gca().set_xlim([minimum, maximum])

        tmpfile = BytesIO()
        plt.savefig(tmpfile, format='png')
        plt.clf()
        plt.close()
        return base64.b64encode(tmpfile.getvalue()).decode('ascii')

    def handle_request(self, data=None):
        self.offline_machines = self.dal.get_older_records()
        self.online_machines = self.dal.get_all_recent_updated_records()
        self.graph_data_mem = self._generate_graph_base64_string('mem_used_perc', 'Used memory percentage', 'Machines')
        self.graph_data_cpu = self._generate_graph_base64_string('cpu_perc', 'Used cpu percentage', 'Machines')

        self._get_random_quote()
        self.online_machines = self._prepare_data(self.dal.get_all_recent_updated_records())
        self.offline_machines = self._prepare_data(self.dal.get_older_records())

        print(self.template.render(
            online_machines=self.online_machines,
            offline_machines=self.offline_machines,
            random_quote_content=self.random_quote_content,
            random_quote_author=self.random_quote_author,
            graph_data_mem=self.graph_data_mem,
            graph_data_cpu=self.graph_data_cpu,
        ))
