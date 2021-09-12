from os import walk, path
from fastapi import FastAPI
import re
from tona.utils import logger
def registry(apps_dir) -> FastAPI:
    v1 = FastAPI()
    for (dirpath, dirnames, filenames) in walk(apps_dir):
        for filename in filenames:
            filepath = f"{path.join(dirpath, filename)}"
            if re.search("router.py$", filepath):
                modelpath = filepath.replace(".py", "").replace("/", ".")
                modelimport = __import__(modelpath)
                dirs = modelpath.replace('tona.', '').split('.')
                for dir in dirs:
                    if getattr(modelimport, dir):
                        modelimport = getattr(modelimport, dir)
                prefix = dirpath.replace('_','-')
                prefix = f"/{prefix.split('/')[-1]}"
                if getattr(modelimport, 'v1'):
                    v1.include_router(getattr(modelimport, 'v1'), prefix=prefix)
    for route in v1.routes:
        logger.info("Route %s: %s",route.name, route.path)
    return v1
