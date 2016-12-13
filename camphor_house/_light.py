import json
import requests
import os
from logging import getLogger,StreamHandler,DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

dir = os.path.dirname(__file__)
path = '%s/hue_settings.json' % dir
with open(path) as fp:
    j = json.load(fp)
# Constants
API_ENDPOINT = j["API_ENDPOINT"]
ACCESS_KEY = j["ACCESS_KEY"]
USER = j["USER"]
PASS = j["PASS"]


class Light(object):
    def __init__(self, light_id):
        self.__auth = (USER, PASS)
        self.__url = '%s/%s/lights/%d/state/' % (API_ENDPOINT, ACCESS_KEY, light_id)

    def __request(self, method, headers=None, data=None):
        try:
            r = requests.request(method=method, url=self.__url, auth=self.__auth, headers=headers, data=data)
            # check status_code
            if r.status_code != 200:
                return 'Error w/STATUS_CODE: %d' % r.status_code
                logger.error(e)
            return r.json()

        except requests.exceptions.RequestException as e:
            logger.error(e)

    @property
    def status(self):
        return self.__request(method='GET')

    def turn_on(self):
        headers = {'Content-type': 'application/json'}
        body = json.dumps({'on': True})
        return self.__request(method='PUT', headers=headers, data=body)

    def turn_off(self):
        headers = {'Content-type': 'application/json'}
        body = json.dumps({'on': False})
        return self.__request(method='PUT', headers=headers, data=body)
