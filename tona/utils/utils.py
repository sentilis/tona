import os
import hashlib
import logging

def md5sum(fn):
    hasher = hashlib.md5()
    if os.path.isfile(fn):
        with open(fn, 'rb') as f:
            hasher.update(f.read())
            return hasher.hexdigest()

    return hashlib.sha1(fn.encode("utf-8")).hexdigest()


logging.basicConfig(level=logging.INFO, format='%(levelname)s:     %(message)s')
logger = logging.getLogger("tona")
