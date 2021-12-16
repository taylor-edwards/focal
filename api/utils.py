import hashlib
import json5 as json

def load_config(prop=None):
    config = None
    # TODO: only reload this file every X seconds, instead of on every use
    with open('/config.json', 'r') as f:
        config = json.load(f)
    if config is not None and prop is not None:
        return config[prop]
    return config

def hash_file(file):
    BUFFER_SIZE = 65536 # 64kb chunks
    md5 = hashlib.md5()
    while True:
        data = file.read(BUFFER_SIZE)
        if not data:
            break
        md5.update(data)
    return md5

def read_extension(file_name):
    return file_name.rsplit('.', 1)[1].lower()

def del_prop(object, property):
    if property in object:
        del object[property]
