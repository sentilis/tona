from fastapi import FastAPI


v1 = FastAPI()

@v1.get('/')
def home():
    return {'version': "0.1.0" }

