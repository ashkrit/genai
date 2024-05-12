## Application Config loader

import json

class Config:
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load()

    def load(self):
        with open(self.config_file) as f:
            self.config = json.load(f)
        return self.config
    
    def get(self, key):
        return self.config[key]