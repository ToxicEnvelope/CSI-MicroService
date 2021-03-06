import requests
import json


class BaseAPI:
    __HTTP__ = "http://"
    __HTTPS__ = "https://"
    __BASE_URL__ = ""
    __headers__ = {}

    def __init__(self, url):
        self.__BASE_URL__ = url

    def get(self, url, **kwargs):
        response = requests.get(url=url, *kwargs)
        return response
