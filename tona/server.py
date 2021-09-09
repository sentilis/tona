import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tona.core import init_db, registry_db, registry_router, Config

app = FastAPI(title="Tona API")
config = Config()

if os.path.exists('tona'):
    config.run_main = False

app.state.config = config
origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:5002",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db(config.db_sqlite)
registry_db(config.apps_dir)

app.mount('/api/v1', registry_router(config.apps_dir))
app.mount("/client", StaticFiles(directory=f"{os.path.join(config.templates_dir, 'client')}"), name="client")
app.mount('/', StaticFiles(directory=f'{config.templates_dir}', html=True), name='home')
