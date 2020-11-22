import json
from utils import path

class Cache:
    def __init__(self, file):
        self.filename = path + f'cache/{file}'

    def _test_if_empty(self):
        with open(self.filename) as f:
            try:
                data = json.load(f)
            except:  # if the file is somehow 0 bytes
                with open(self.filename, 'w') as ff:
                    data = json.loads('{}')
                    json.dump(data, ff, indent=3)
                    return True
        return False

    def cached(self, key):
        """
        Check if the question has already been stored.
        """
        empty = self._test_if_empty()
        if empty: return False

        with open(self.filename) as f:
            data = json.load(f)
        if key in data.keys():
            return True
        return False

    def all(self):
        """
        Return the whole database.
        """
        empty = self._test_if_empty()
        if empty: return {}

        with open(self.filename) as f:
            data = json.load(f)

        return data

    def store(self, dictionary):
        """
        Add to the database.
        """
        empty = self._test_if_empty()
        if empty: return {}

        with open(self.filename) as f:
            data = json.load(f)

        data.update(dictionary)

        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=3)

    def get(self, key, *keys):
        """
        Retrieve values in the database.
        :param key: A required key to get from the database
        :param keys: Optional other keys to get stacking up from the first key
        For example: get('1', '2', 3) is equal to data['1']['2'][3]
        """
        keys = list(keys)
        keys.insert(0, key)
        with open(self.filename) as f:
            data = json.load(f)
        if not self.cached(key):
            return ""
        evalulated = 'data' + ''.join([f'[{ascii(keyy) if type(keyy) == str else keyy}]' for keyy in keys])
        return eval(evalulated)