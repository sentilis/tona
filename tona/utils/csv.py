import csv
import os
import base64

def build_csv(storage, name, data, **kwargs):
    fpath = storage
    if not os.path.exists(fpath):
        os.makedirs(fpath)
    fpath = os.path.join(fpath, name)
    with open(fpath, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    if kwargs.get("b64", False):
        with open(fpath, 'rb') as csvfile:
            return base64.b64encode(csvfile.read())
    return fpath
