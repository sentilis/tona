import peewee
from os import walk, path
import re

db = peewee.SqliteDatabase(None)

def init(name):
    db.init(name)
    db.connect()

def registry(apps_dir):
    tables = []
    for (dirpath, dirnames, filenames) in walk(apps_dir):
        if re.search("/models$", dirpath):
            for filename in filenames:
                if filename != '__init__.py':
                    filepath = path.join(dirpath, filename)
                    modelpath = filepath.replace(".py", "").replace("/", ".")
                    modelimport = __import__(modelpath)
                    classname =  ''.join(x.capitalize() or '_' for x in filename.replace('.py','').split('_'))
                    
                    dirs = modelpath.replace('tona.','').split('.')
                    for dir in dirs:
                        if getattr(modelimport, dir):
                            modelimport = getattr(modelimport, dir)                    
                    if getattr(modelimport, classname):
                        tables.append(getattr(modelimport, classname))
    db.create_tables(tables)