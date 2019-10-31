import os
import socket
import time
import urllib.parse
import urllib.request
from datetime import datetime
import psutil
import schedule

from utils.payload import PayLoad

HOST_NAME = socket.gethostname()
UNIQUE_IDENTIFIER = f'{HOST_NAME}-{socket.gethostbyname(HOST_NAME)}'
URL = os.environ.get('DESTINATION_HOST', 'http://localhost:80/cgi-bin/src/management.py')


def job():
    payload = PayLoad(
        identifier=UNIQUE_IDENTIFIER,
        last_updated=int(time.time()),
        cpu_count=psutil.cpu_count(),
        cpu_freq=int(psutil.cpu_freq().current),
        cpu_perc=psutil.cpu_percent(),
        mem_total=psutil.virtual_memory().total,
        mem_available=psutil.virtual_memory().available,
        mem_used=psutil.virtual_memory().used,
        mem_free=psutil.virtual_memory().free,
        mem_used_perc=psutil.virtual_memory().percent,
        swap_total=psutil.swap_memory().total,
        swap_used=psutil.swap_memory().used,
        swap_free=psutil.swap_memory().free,
        swap_used_perc=psutil.swap_memory().percent,
    ).to_dict()
    data = urllib.parse.urlencode(payload)
    data = data.encode('ascii')
    req = urllib.request.Request(URL, data)
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print(f'{datetime.fromtimestamp(int(time.time()))} - Successful request', flush=True)
    except Exception as e:
        print(f'{datetime.fromtimestamp(int(time.time()))} - Some kind of error occurred!\n{e}', flush=True)


if __name__ == '__main__':
    job()
    schedule.every(15).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
