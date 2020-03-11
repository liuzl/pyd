# pyd: An updateable dict service for Python3, multi-pattern match

## Introduction

`pyd` is a python3 package of dict service, multi-pattern match, we also have a Golang version [https://github.com/liuzl/d](https://github.com/liuzl/d).

## Install

```sh
pip install pydict-cedar
```

## Usage

```python
from pydict import Dict

d = Dict("data")

# insert data to dict
d["中国"] = {"Country": "中华人民共和国"}
d["中国人民"] = {"People": "中华人民共和国合法公民"}
d.save()

# fetch item in dict
x = d['中国']
print(x)

# match items in dict for a sentence
ret = d.multi_match("中国人民是伟大的人民,中国近年来的发展有目共睹")
print(ret)
ret = d.multi_max_match("中国人民是伟大的人民,中国近年来的发展有目共睹")
print(ret)
```
