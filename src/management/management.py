#!/usr/bin/python3.6
import cgi
import cgitb
import os
from utils.status import RequestStatus
from management.post_handler import PostHandler
from management.get_handler import GetHandler
from utils.cgi_to_dict import cgi_field_storage_to_dict

cgitb.enable()

REQUEST_METHOD = os.environ['REQUEST_METHOD']

if REQUEST_METHOD == 'GET':
    print('Content-Type:text/html\r\n\r\n')
    try:
        get_handler = GetHandler()
        get_handler.handle_request()
    except Exception as e:
        print(RequestStatus(500, 'Internal server errors!\nCheck the apache logs for more information.' + str(e)))
elif REQUEST_METHOD == 'POST':
    print('Content-Type:text/html\r\n\r\n')
    try:
        data = cgi.FieldStorage()
        post_handler = PostHandler()
        data_dict = cgi_field_storage_to_dict(data)
        post_handler.handle_request(data_dict)
    except Exception as e:
        print(RequestStatus(500, 'Internal server errors!\nCheck the apache logs for more information.' + str(e)))
else:
    print(RequestStatus(405, 'Request method not allowed!\nTry GET or POST.'))
