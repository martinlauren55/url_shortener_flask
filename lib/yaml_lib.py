import yaml


class YamlManager:
    def __init__(self, path):
        """path = path to db"""
        self._path = path

    def save(self, key: str, value: str):
        with open(self._path, 'a') as f:
            yaml.dump([{"short_link": key, "full_link": value}], f, default_flow_style=False)

    def get_keys(self):
        try:
            with open(self._path) as f:
                dictionary_data = yaml.safe_load(f)
            t = []
            for i in dictionary_data:
                t.append(i['short_link'])
            return t
        except Exception:
            return False

    def get_by_key(self, key):
        with open(self._path) as f:
            dictionary_data = yaml.safe_load(f)
        for i in dictionary_data:
            if key == i['short_link']:
                return i['full_link']
        return None