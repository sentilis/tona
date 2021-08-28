import os
import yaml

class Config:

    def __init__(self, filename) -> None:
        self.default()
        if filename and os.path.exists(filename):
            with open(filename) as stream:
                data = yaml.safe_load(stream)
                self.load_conf(data)

    def default(self) -> None:
        self.env = 'development'

        self.server_port = 5001
        self.server_host = '0.0.0.0'
        self.server_reload = False

        self.log_level = 'debug'


    def load_conf(self, data: dict) -> None:
        print(data)
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
