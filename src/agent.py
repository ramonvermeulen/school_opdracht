import urllib.request
import urllib.parse
import platform
import schedule
import time

URL = '127.0.0.1/cgi/management_script.py'


def job():
    ...


if __name__ == '__main__':
    schedule.every(30).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
