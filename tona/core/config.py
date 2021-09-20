import os
from functools import lru_cache
from pydantic import BaseSettings
import click


class Config(BaseSettings):
    
    env: str = 'production'
    
    server_port: int = 5001
    server_host: str = '0.0.0.0'
    server_reload: bool = False
    
    log_level: str = 'debug'
    
    data: str = os.path.join(click.get_app_dir("tona"), 'data')
    
    db_name: str = 'tona.db'

    run_main: bool = True


    @property
    def drive(self) -> str:
        path = os.path.join(self.data, 'drive')
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @drive.setter
    def drive(self, val):
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
        if not os.path.exists(self.data):
            os.makedirs(self.data)
        return f"{os.path.join(self.data, self.db_name)}"

    @db_sqlite.setter
    def db_sqlite(self, val):
        pass


@lru_cache
def get_config():
    return Config()