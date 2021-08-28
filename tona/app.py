import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from tona.router import v1

app = FastAPI(title="Tona API")

static_path = ''
if os.path.exists('tona'):
    static_path = 'tona/'

app.mount('/api/v1', v1)
app.mount("/client", StaticFiles(directory=f"{static_path}template/client"), name="client")
app.mount('/', StaticFiles(directory=f'{static_path}template', html=True), name='home')

