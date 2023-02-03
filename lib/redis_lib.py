import redis


class RedisManager:
    def __init__(self, host, port, db=0, decode_responses=True):
        self._host = host
        self._port = port
        self._db = db

    def __enter__(self):
        """ Opening connection with Redis"""
        self._redis_cli = redis.Redis(host=self._host, port=self._port, db=self._db)
        return self

    def key_exists(self, key):
        """Returns TRUE if key exists"""
        if self._redis_cli.exists(key) == 1:
            return True
        else:
            return False

    def save(self, key, value):
        try:
            self._redis_cli.set(name=key, value=value)
        except Exception as e:
            print(f'Error: {e}')

    def get_by_key(self, key):
        """Return value by key"""
        try:
            return self._redis_cli.get(key).decode('UTF-8')
        except Exception as e:
            print(e)
            return None

    def get_keys(self):
        _t = []
        for i in self._redis_cli.keys(pattern='*'):
            _t.append(i.decode('UTF-8'))
        return _t

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Closing the connection """
        self._redis_cli.close()
        if exc_val:
            raise
