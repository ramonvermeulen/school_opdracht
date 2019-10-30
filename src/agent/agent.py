import urllib.request
import urllib.parse
from utils.payload import PayLoad
import schedule
import time
import os
import psutil
import socket
import uuid

HOST_NAME = socket.gethostname()
UNIQUE_IDENTIFIER = f'{HOST_NAME}-{socket.gethostbyname(HOST_NAME)}'
URL = os.environ.get('DESTINATION', 'http://localhost:80/cgi-bin/src/management.py')


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
    with urllib.request.urlopen(req) as response:
        if response.status == 200:
            print(True)


if __name__ == '__main__':
    job()
    schedule.every(15).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
