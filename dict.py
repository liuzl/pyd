import os
import pickle
import lsm
import pycedar

class Dict(object):
    def __init__(self, path: str):
        if not os.path.exists(path): os.makedirs(path)
        self.path = path
        self.kv_path = os.path.join(self.path, "kv.ldb")
        self.cedar_path = os.path.join(self.path, 'cedar')
        self.kv = lsm.LSM(self.kv_path)
        self.cedar = pycedar.dict()
        self.cedar.load(self.cedar_path)    

    def __getitem__(self, key: str):
        return self.get(key)
    def __setitem__(self, key: str, values: dict):
        self.replace(key, values)
    def __delitem__(self, key: str):
        self.delete(key)


    def get(self, key: str, default=None):
        try:
            v = self.kv[key]
            return pickle.loads(v)
        except KeyError as e:
            return default

    def delete(self, key: str):
        del self.kv[key]
        del self.cedar[key]

    def update(self, key: str, values: dict):
        key = key.strip()
        if key == "": raise KeyError("Empty key")
        if values is None or len(values) == 0:
            raise ValueError("Empty value")
        old = self.get(key)
        if old is None:
            raise KeyError("Key {} not found".format(key))
        for k, v in values.items():
            old[k] = v
        self.replace(key, old)

    def replace(self, key: str, values: dict):
        key = key.strip()
        if key == "": raise KeyError("Empty key")
        if values is None or len(values) == 0:
            raise ValueError("Empty value")
        self.cedar[key] = len(values)
        self.kv[key] = pickle.dumps(values)

    def prefix_match(self, text: str):
        pass
    def multi_match(self, text: str):
        pass
    def multi_max_match(self, text: str):
        pass


if __name__ == "__main__":
    d = Dict("data")
    value = d.get("中国")
    print(value)
    d["中国"] = {"China": "中华人民共和国"}
    x = d['中国']
    print(x)
    del d['中国']
