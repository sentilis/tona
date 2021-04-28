import re

def path_storage():
    pass

def name_constraint(name):
    if not name:
        print("The argument name is required")
        raise SystemExit(1)
    if not isinstance(name, tuple):
        print("The argument name not is tuple")
        raise SystemExit(1)
    return ' '.join(name)


def dt_utc():
    pass

def dt_local():
    pass