import os

basepath = os.path.dirname(globals()["__file__"])
dirname = os.path.abspath(os.path.join(basepath, ".."))




TEMPLATE_DIR=os.path.abspath(os.path.join(dirname,'templates'))

OE_API_BASE_URL = 'http://127.0.0.1:8000/'
OE_API_AUTH_KEY = 'ApiKey admin:1234567890'

OE_API_USER_ENDPOINT = OE_API_BASE_URL+ 'api/v1/user/'
OE_API_APPLICATION_ENDPOINT = OE_API_BASE_URL + 'api/v1/application/'
