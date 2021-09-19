import os
from functools import lru_cache
from fastapi.routing import run_endpoint_function
import yaml
from pydantic import BaseSettings



class Config(BaseSettings):
    
    env: str = 'development'
    
    server_port: int = 5001
    server_host: str = '0.0.0.0'
    server_reload: bool = False
    
    log_level: str = 'debug'
    
    data: str = 'data'
    
    db_name: str = 'tona.db'

    run_main: bool = True


    @property
    def drive_dir(self) -> str:
        return os.path.join(self.data, 'drive')

    @drive_dir.setter
    def drive_dir(self, val):
        pass

    @property
    def apps_dir(self) -> str:
        return 'apps' if self.run_main else 'tona/apps'

    @apps_dir.setter
    def apps_dir(self, val):
        pass

    @property
    def templates_dir(self) -> str:
        return 'templates' if self.run_main else 'tona/templates'

    @templates_dir.setter
    def templates_dir(self, val):
        pass

    @property
    def db_sqlite(self) -> str:
        return f"{os.path.join(self.data, self.db_name)}"

    @db_sqlite.setter
    def db_sqlite(self, val):
        pass

    @property
    def tmp_dir(self) -> str:
        return f"{os.path.join(self.data, 'tmp')}"
    
    @tmp_dir.setter
    def tmp_dir(self, val):
        pass

@lru_cache
def get_config():
    return Config()