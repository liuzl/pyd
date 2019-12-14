import os
import lsm
import pycedar

class Dict(object):
    def __init__(self, path):
        if not os.path.exists(path): os.makedirs(path)
        self.path = path
        self.kv_path = os.path.join(self.path, "kv.ldb")
        self.cedar_path = os.path.join(self.path, 'cedar')
        self.kv = lsm.LSM(self.kv_path)
        self.cedar = pycedar.dict()
        self.cedar.load(self.cedar_path)    

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key, default=None):
        try:
            return self.kv[key]
        except KeyError as e:
            return default

    def __delitem__(self, key):
        self.delete(key)

    def delete(self, key):
        del self.kv[key]
        del self.cedar[key]

    def update(self, key, values):
        pass
    def replace(self, key, values):
        pass

    def prefix_match(self, text):
        pass
    def multi_match(self, text):
        pass
    def multi_max_match(self, text):
        pass


if __name__ == "__main__":
    d = Dict("data")
    value = d.get("中国")
    print(value)
    x = d['中国']
    del d['中国']
