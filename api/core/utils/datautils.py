import json;
from dataclasses import astuple;

def relicjson(obj):
    return json.dumps(obj, separators=",:", default=astuple);

def read_datafile(name):
    return json.dumps(json.load(open(name)), separators=",:");
