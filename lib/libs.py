import datetime
import random
import uuid
import os
import re

import requests
import json


class Config:
    """Read json and return objects"""

    def __init__(self, path):
        """path - path to pref.json"""
        self._path = path
        with open(self._path, "r") as f:
            js = json.loads(f.read())
            if os.getenv('STORAGE_TYPE') == 'yaml':
                storage = 'yaml'
            elif os.getenv('STORAGE_TYPE') == 'redis':
                storage = 'redis'
            else:
                storage = js['storage']

            name_yaml_bd = js['name_yaml_bd']

            if os.getenv('REDIS_HOST') == 'redis':
                redis_host = 'redis'
            elif os.getenv('REDIS_HOST') == 'localhost':
                redis_host = 'localhost'
            else:
                redis_host = js['redis_host']
            redis_port = js['redis_port']
            redis_db = js['redis_db']
            domen_name = js['domen_name']

        self.storage = storage
        self.name_yaml_bd = name_yaml_bd
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.domen_name = domen_name


class LinkGenerator:
    """Generating link and returns a new in new_link variable
    generate_method  = "timestamp" or "uuid4" (by default) return six characters
    """

    def __init__(self, generate_method='uuid4'):
        self._generate_method = generate_method

        if self._generate_method == 'uuid4':
            self.new_link = self._uuid4()

        if self._generate_method == 'timestamp':
            self.new_link = self._timestamp()

    def _timestamp_now(self):
        """Return timestamp datetime now"""
        return str(datetime.datetime.now().timestamp())

    def _random_lower(self):
        """Return random letters lowercase"""
        return chr(random.randint(97, 122))

    def _random_upper(self):
        """Return random letters Uppercase"""
        return chr(random.randint(65, 90))

    def _timestamp(self):
        ch = str(self._random_upper() + self._random_lower())
        f = self._timestamp_now().replace('.', ch)[10:]
        t = f[:3] + f[-3:]
        return t

    def _uuid4(self):
        """Returns first six characters"""
        return str(uuid.uuid4())[:6]


class CheckUrl:
    """Return True if link exist"""

    def __init__(self, url: str):
        self._url = url
        if self._parse_protocol(self._url):
            self.is_link = self._check_url(self._url)
        else:
            if self._parse_www(self._url):
                self._url = str('http://' + self._url)
                self.is_link = self._check_url(self._url)
            else:
                self._url = str('http://www.' + self._url)
                self.is_link = self._check_url(self._url)

    def _parse_protocol(self, link: str) -> bool:
        """ return True if https or http """
        pattern = r'(https|http)'
        res = re.match(pattern, link)
        if res:
            return True
        else:
            return False

    def _parse_www(self, link: str) -> bool:
        """ return True if www """
        pattern = r'(www)'
        res = re.match(pattern, link)
        if res:
            return True
        else:
            return False

    def _check_url(self, url: str) -> bool:
        try:
            response = requests.head(url)
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False
