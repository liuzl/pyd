import os
import pickle
import lsm
import pycedar

class Dict(object):
    def __init__(self, path: str):
        if not os.path.exists(path): os.makedirs(path)
        self.path = path
        self.kv_path = os.path.join(self.path, "kv.ldb")
        self.cedar_path = os.path.join(self.path, 'cedar.dat')
        self.kv = lsm.LSM(self.kv_path)
        self.cedar = pycedar.dict()
        self.cedar.load(self.cedar_path)    

    def __getitem__(self, key: str):
        return self.get(key)
    def __setitem__(self, key: str, values: dict):
        self.replace(key, values)
    def __delitem__(self, key: str):
        self.delete(key)
    def __len__(self):
        return len(self.cedar)


    def get(self, key: str, default=None):
        try:
            v = self.kv[key]
            return pickle.loads(v)
        except KeyError as e:
            return default

    def delete(self, key: str):
        del self.kv[key]
        del self.cedar[key]

    def insert(self, key: str, values: dict):
        key = key.strip()
        if key == "": raise KeyError("Empty key")
        if values is None or len(values) == 0:
            raise ValueError("Empty value")
        old = self.get(key, {})
        for k, v in values.items():
            if k not in old:
                old[k] = set([v])
            else:
                old[k] = set(old[k]) | set([v])
        self.replace(key, old)

    def update(self, key: str, values: dict):
        key = key.strip()
        if key == "": raise KeyError("Empty key")
        if values is None or len(values) == 0:
            raise ValueError("Empty value")
        old = self.get(key)
        if old is None:
            old = values
        else:
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
        text = text.strip()
        if text == "": return None
        prefixs = self.cedar.trie.common_prefix_search(text)
        if len(prefixs) == 0: return None
        sets = {}
        for v in prefixs:
            word = v[0]
            values = self.get(word)
            for typ, val in values.items():
                tv = "{}_{}".format(typ, val)
                if tv not in sets or len(word) > len(sets[tv][0]):
                    sets[tv] = (word, typ, val)
        ret = {}
        for _, v in sets.items():
            if v[0] not in ret: ret[v[0]] = {v[1]: v[2]}
            else: ret[v[0]][v[1]] = v[2]
        return ret

    def multi_match(self, text: str):
        text = text.strip()
        if text == "": return None
        ret = {}
        for i in range(len(text)):
            hits = self.prefix_match(text[i:])
            if hits is None: continue
            for k, v in hits.items():
                if k not in ret:
                    ret[k] = {"value": v, "hits": []}
                ret[k]["hits"].append({"start": i, "end": i+len(k)})
        return ret

    def multi_max_match(self, text: str):
        text = text.strip()
        if text == "": return None
        ret = {}
        i, l = 0, len(text)
        while i < l:
            hits = self.prefix_match(text[i:])
            if hits is None:
                i += 1
                continue
            key = ""
            for k, _ in hits.items():
                if len(k) > len(key):
                    key = k
            if key not in ret:
                ret[key] = {"value": hits[key], "hits": []}
            ret[key]["hits"].append({"start": i, "end": i+len(key)})
            i += len(key)
        return ret

    def save(self):
        self.cedar.save(self.cedar_path)

if __name__ == "__main__":
    d = Dict("data")
    d["中国"] = {"Country": "中华人民共和国"}
    d["中国人民"] = {"People": "中华人民共和国合法公民"}
    d.save()
    x = d['中国']
    print(x)
    ret = d.multi_match("中国人民是伟大的人民,中国近年来的发展有目共睹")
    print(ret)
    ret = d.multi_max_match("中国人民是伟大的人民,中国近年来的发展有目共睹")
    print(ret)
