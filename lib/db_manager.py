from lib.redis_lib import RedisManager
from lib.libs import LinkGenerator


class DB_Manager:
    """ Main class for Read, Write, and Other methods with DB..."""

    def __init__(self, config_class, yaml_manager_class):
        self._conf = config_class
        self._yaml_manager = yaml_manager_class

    def key_exist(self, key):
        """Return True if key EXIST else False"""
        if self._conf.storage == 'yaml':
            if self._yaml_manager.get_keys():
                if key in self._yaml_manager.get_keys():
                    return True
            else:
                return False
        if self._conf.storage == 'redis':
            with RedisManager(host=self._conf.redis_host, port=self._conf.redis_port, db=self._conf.redis_db) as t:
                if t.key_exists(key):
                    return True
                else:
                    return False

    def get_by_key(self, key:str) -> str:
        """Return value by key"""
        if self._conf.storage == 'yaml':
            return self._yaml_manager.get_by_key(key)

        if self._conf.storage == 'redis':
            with RedisManager(host=self._conf.redis_host, port=self._conf.redis_port, db=self._conf.redis_db) as t:
                return t.get_by_key(key)

    def save(self, key: str, value: str):
        if self._conf.storage == 'yaml':
            self._yaml_manager.save(key=key, value=value)

        if self._conf.storage == 'redis':
            with RedisManager(host=self._conf.redis_host, port=self._conf.redis_port, db=self._conf.redis_db) as t:
                t.save(key=key, value=value)

    def get_keys(self):
        if self._conf.storage == 'yaml':
            return self._yaml_manager.get_keys()
        if self._conf.storage == 'redis':
            with RedisManager(host=self._conf.redis_host, port=self._conf.redis_port, db=self._conf.redis_db) as t:
                return t.get_keys()

    def unique_link(self, generate_method='uuid4'):
        if generate_method =='uuid4':
            method = 'uuid4'
        if generate_method == 'timestamp':
            method = 'timestamp'
        while True:
            link = LinkGenerator(generate_method=method).new_link
            if not self.key_exist(link):
                return link

    def value_exists(self, value: str):
        keys = self.get_keys()
        if keys:
            for k in keys:
                if value == self.get_by_key(k):
                    return k
        else:
            return False


if __name__ == "__main__":

    from pathlib import Path
    from lib.libs import Config, LinkGenerator
    from lib.yaml_lib import YamlManager
    from lib.redis_lib import RedisManager

    conf = Config(Path("..", "pref.json"))
    yaml_manager = YamlManager(path=Path("..", "data", conf.name_yaml_bd))
    k = DB_Manager(conf, yaml_manager)
    print(k.value_exists('https://gitlab.mai.ru/PolyakovSV'))