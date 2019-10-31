FROM python:3

ADD . /usr/srv/agent

RUN ["pip", "install", "-r", "/usr/srv/agent/requirements.txt"]
CMD ["stdbuf", "-oL", "python", "/usr/srv/agent/agent.py"]