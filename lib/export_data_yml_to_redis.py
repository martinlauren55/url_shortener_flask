from lib.redis_lib import RedisManager
from lib.yaml_lib import YamlManager
from lib.libs import Config

from pathlib import Path




def export_data(yaml_manager, conf):
    try:
        for key in yaml_manager.get_keys():
            value = yaml_manager.get_by_key(key)

            with RedisManager(conf.redis_host, conf.redis_port, conf.redis_db) as f:
                f.save(key, value)
            print(f"Successfully added key: {key}, value: {value}")
    except Exception:
        return False


if __name__ == "__main__":
    conf = Config(Path("..", "pref.json"))
    yaml_manager = YamlManager(path=Path("..", "data", conf.name_yaml_bd))

    export_data(yaml_manager, conf)
