import os
import yaml

class Config:

    def __init__(self) -> None:
        self.default()
        self.run_main = True

    def default(self) -> None:
        self.env = os.getenv('ENV') or 'development'

        self.server_port = int(os.getenv('SERVER_PORT', 0)) or 5001
        self.server_host = os.getenv('SERVER_HOST') or '0.0.0.0'
        self.server_reload = os.getenv('SERVER_RELOAD') or False

        self.log_level = os.getenv('LOG_LEVEL') or 'debug'

        self.data = os.getenv('DATA') or 'data'

        self.db_name = os.getenv('DB_NAME') or 'tona.db'

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

    def load_yaml(self, filename) -> None:
        data: dict = {}
        if filename and os.path.exists(filename):
            with open(filename) as stream:
                data = yaml.safe_load(stream)

        for attr in ['env']:
            if data.get(attr):
                setattr(self, attr, data.get(attr))

        config = {
            'server': ['port', 'host', 'reload'],
            'log': ['level']
        }
        for conf in config.keys():
            vals = data.get(conf, {})
            for attr in config.get(conf):
                if vals.get(f"{attr}"):
                    setattr(self, f"{conf}_{attr}", vals.get(attr))
